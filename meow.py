import requests
import math
import plotly.express as px

class Battler():
    """A battler character in manarion"""
    def __init__(self, name, tax, mob_shift):
        """Initializing name, tax, data from market, api."""
        self.name = name
        self.tax = tax
        self.mob_shift = mob_shift
        self._data()
        self._market_data()
        self._market_prices()
        self._extracting_values()
        self._computing_values()

    def _data(self):
        """Fetching player data."""
        url=f"https://api.manarion.com/players/{self.name}"
        r = requests.get(url)
        if r.status_code == 200:
            self.data = r.json()
            print("Player data saved successfully.")
        else:
            print(f"Failed to fetch player data: {r.status_code}")
            return None    
    
    def _market_data(self):
        """ Make an api call, and store the response."""
        url= "https://api.manarion.com/market"
        r = requests.get(url)

        if r.status_code == 200:
            self.marketdata = r.json()
            print("Market data saved successfully.")
        else:
            print(f"Failed to fetch market data: {r.status_code}")
            return None
    
    def _market_prices(self):
        """Creates market prices."""
        self.res_price = (self.marketdata['Sell'].get('7',math.inf)+self.marketdata['Sell'].get('8',math.inf)+self.marketdata['Sell'].get('9',math.inf))/3
        self.spell_tome_price = (self.marketdata['Sell'].get('13',math.inf)+self.marketdata['Sell'].get('14',math.inf)+self.marketdata['Sell'].get('15',math.inf))/3
        self.shard_price= (self.marketdata['Buy'].get('2',0)+self.marketdata['Sell'].get('2',math.inf))/2
        self.mana_tome_price = (self.marketdata['Buy'].get('16',0)+self.marketdata['Sell'].get('16',math.inf))/2
        
    def _extracting_values(self):
        """Extracts values for different playerboosts."""
        self.dust_boost = self.data['TotalBoosts'].get('121',0)
        self.dust_codex = self.data['TotalBoosts'].get('101',0)
        self.dc = self.data['BaseBoosts'].get('161',0)
        self.mob_strength = self.data['Enemy']+150
        self.cur_ward_upgs = self.data['BaseBoosts'].get('2',0)
        self.cur_health = self.data['BaseBoosts'].get('45',0)
        self.cur_mana = self.data['BaseBoosts'].get('48',0)
        self.shield_rank = self.data['BaseBoosts'].get('24',0)

    def _computing_values(self):
        """Computes values from extracted data."""
        self.dust_income = (0.0001*self.mob_strength**2 + self.mob_strength**1.2+10*self.mob_strength)*(1.01**((self.mob_strength-150000)/2000))*(1+self.dust_boost/100)*(1+self.dust_codex/100)*(1+self.dc*0.002)*(1-self.tax/100)*28800
        self.mob_strength_boosted = self.mob_strength+self.mob_shift
        self.dust_income_boosted = (0.0001*self.mob_strength_boosted**2 + self.mob_strength_boosted**1.2+10*self.mob_strength_boosted)*(1.01**((self.mob_strength_boosted-150000)/2000))*(1+self.dust_boost/100)*(1+self.dust_codex/100)*(1+self.dc*0.002)*(1-self.tax/100)*28800
        self.extra_income = self.dust_income_boosted - self.dust_income
        self.gear_ward = 0
        for slot in ('2', '3', '4', '5', '6'):
            item = self.data['Equipment'].get(slot)
            if not item:
                continue
            boosts = item.get('Boosts', {})
            self.gear_ward += boosts.get('9',0) * (item.get('Infusions',0) * 0.05 + 1)
        self.mana_shield = self.data['TotalBoosts'].get('7',1)*self.data['TotalBoosts'].get('48',1)*self.data.get('Level',1)*(self.data['BaseBoosts'].get('24',0)/100)
        self.health_points = self.data['TotalBoosts'].get('4',1)*self.data['TotalBoosts'].get('45',1)*(self.data.get('Level')+9)
        self.cost_of_ten_percent_health = ((self.cur_health*1.1)*(self.cur_health*1.1+1)-(self.cur_health*(self.cur_health+1)))*self.shard_price
        self.cost_of_ten_percent_mana = ((self.cur_mana*1.1)*(self.cur_mana*1.1+1)-(self.cur_mana*(self.cur_mana+1)))*self.shard_price
        self.cost_of_ten_pc_shield = (round(self.shield_rank*1.1)*((round(self.shield_rank*1.1)+1))/2-((self.shield_rank*(self.shield_rank+1))/2))*self.mana_tome_price


    def dust_collector(self):
        """Dust collector roi."""
        cost_of_next_DC = 7500000*(self.dc+1)**3+3*10000*(self.dc+1)**3*self.res_price
        income_increase_from_dc = self.dust_income*0.002
        roi_dc =cost_of_next_DC/income_increase_from_dc
        return roi_dc
    
# 10% Damage increase with sp, tome, shardboost
# Spellpower
    def spellpower(self):
        """Spell power roi."""
        gear_sp = self.data['Equipment']['1']['Boosts'].get('8',0)*(self.data['Equipment']['1'].get('Infusions',0)*0.05+1)
        cur_sp_upg = self.data['BaseBoosts'].get('1',0)
        m = math.ceil(
            (-1+math.sqrt(1+4*(1.1*cur_sp_upg*(cur_sp_upg+1)+0.2*gear_sp)))/2
        )
        cost_of_upg_req = round((m*(m+1)*(2*m+1))/6*1000-(cur_sp_upg*(cur_sp_upg+1)*(2*cur_sp_upg+1))/6*1000)
        roi_sp = cost_of_upg_req/self.extra_income
        return roi_sp

# Spell tome
    def spell_tome(self):
        """Spell tome roi."""
        keys = ['21', '22', '23']
        current_spell_tome_rank = max(self.data['BaseBoosts'].get(k, 0)for k in keys)
        cost_of_next_tome_rank = (current_spell_tome_rank+1)**3*self.spell_tome_price
        roi_spell_tome = cost_of_next_tome_rank/self.extra_income
        return roi_spell_tome

# Shard
    def shard(self):
        """Shard boost roi."""
        keys = ['40','41','42','43','44','47','49','50']
        lowest_shard_upgrade_investment = min(self.data['BaseBoosts'].get(k,0)for k in keys)
        cost_of_ten_percent_shard = ((lowest_shard_upgrade_investment*1.1)*(lowest_shard_upgrade_investment*1.1+1)-(lowest_shard_upgrade_investment*(lowest_shard_upgrade_investment+1)))*self.shard_price
        roi_shard = cost_of_ten_percent_shard/self.extra_income
        return roi_shard

# 10% tank increase with ward%, ward#, resistance, ehp
# ward%
    def ward_shard(self):
        """Ward shard boost roi."""
        current_ward_percent = self.data['BaseBoosts'].get('46',0)
        cost_of_ten_percent_wardshard = ((current_ward_percent*1.1)*(current_ward_percent*1.1+1)-(current_ward_percent*(current_ward_percent+1)))*self.shard_price
        roi_ward_shard = cost_of_ten_percent_wardshard/self.extra_income
        return roi_ward_shard

# ward#
    def ward(self):
        """Ward roi."""
        n = math.ceil(
            (-1+math.sqrt(1+4*(1.1*self.cur_ward_upgs*(self.cur_ward_upgs+1)+0.2*self.gear_ward)))/2
        )
        cost_ward_flat = (n*(n+1)*(2*n+1))/6*1000-(self.cur_ward_upgs*(self.cur_ward_upgs+1)*(2*self.cur_ward_upgs+1))/6*1000
        roi_ward_flat = cost_ward_flat/self.extra_income
        return roi_ward_flat

# resistances
# using 10 upgrades, even tho 10 upgrades are bigger impact than 10%, around 10,5%
# doesn't really matter, this is a bad upgrade for everyone i have seen
    def resistance(self):
        """Resistance roi."""
        keys = ['83', '84', '85']
        cur_res_tome_rank = max(self.data['BaseBoosts'].get(k, 0)for k in keys)
        cost_of_plus_ten_res = (((cur_res_tome_rank+10)*(cur_res_tome_rank+11))**2-(cur_res_tome_rank*(cur_res_tome_rank+1))**2)*self.spell_tome_price
        roi_resistance = cost_of_plus_ten_res/self.extra_income
        return roi_resistance

# ehp
# Health
    def health(self):
        """Health roi."""
        ehp_with_ten_pc_health = self.mana_shield+self.health_points*1.1
        ehp_inc_from_ten_pc_health = ((ehp_with_ten_pc_health/(self.mana_shield+self.health_points))-1)*100
        roi_health = ((10/ehp_inc_from_ten_pc_health)*self.cost_of_ten_percent_health)/self.extra_income
        return roi_health
# Mana shard
    def mana(self):
        """Mana shard roi."""
        ehp_with_ten_pc_mana = self.mana_shield*1.1+self.health_points
        ehp_inc_from_ten_pc_mana =((ehp_with_ten_pc_mana/(self.mana_shield+self.health_points))-1)*100
        roi_mana_shard = ((10/ehp_inc_from_ten_pc_mana)*self.cost_of_ten_percent_mana)/self.extra_income
        return roi_mana_shard
# Mana shield
    def mana_shield_tome(self):
        """Mana shield tome roi."""
        ehp_with_ten_pc_mana = self.mana_shield*1.1+self.health_points
        ehp_inc_from_ten_pc_mana =((ehp_with_ten_pc_mana/(self.mana_shield+self.health_points))-1)*100
        roi_mana_shield = ((10/ehp_inc_from_ten_pc_mana)*self.cost_of_ten_pc_shield)/self.extra_income
        return roi_mana_shield
# Visualization
    def efficiency(self):
        """Making x,y lists for the visualizer."""
        efficiency_list = [("Dust collector",1/self.dust_collector()*100),("Spellpower", 1/self.spellpower()*100),("Tome spell",1/self.spell_tome()*100),("Shards",1/self.shard()*100),("Ward shard",1/self.ward_shard()*100),
                    ("Ward",1/self.ward()*100),("Resistance",1/self.resistance()*100),("Health",1/self.health()*100),("Mana shard",1/self.mana()*100),("Mana shield",1/self.mana_shield_tome()*100)]
        sorted_efficiency_list = sorted(efficiency_list,key=lambda item: item[1])
        self.upgrade_name, self.efficiency_value = zip(*sorted_efficiency_list)

    def visualizer(self):
        """Draws the efficiency of the upgrades as a scatter chart."""
        self.efficiency()
        labels = {'x':'Percent', 'y':''}
        colour_map = {
            "Dust collector": "purple",
            "Spellpower": "red",
            "Tome spell": "red",
            "Shards": "red",
            "Ward shard": "blue",
            "Ward": "blue",
            "Resistance": "blue",
            "Health": "blue",
            "Mana shard": "blue",
            "Mana shield": "blue",
        }
        fig =px.scatter(x=self.efficiency_value, y=self.upgrade_name, title=f"Daily return of different upgrades of {self.name}", labels=labels, size=self.efficiency_value, color=self.upgrade_name, color_discrete_map=colour_map)
        fig.show()
