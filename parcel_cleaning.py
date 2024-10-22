import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

path = 'parcel_clean_final\mathura\Mathura_final.shp'
village = gpd.read_file(path)
print(village)
village['Village'] = 'Nagla Dhanoua'
village.drop(columns = ['VILLAGE'], inplace = True)

#Merging the claims data

claims = pd.read_csv('claim_losses_results_with_cause_of_loss.csv')
claims.drop(columns=['Village', 'KHASRA'], inplace = True)
village_claims = pd.concat([village,claims], axis=1)
# village_claims.

print(village_claims.info())
# print(village_claims['KHASRA'].isna().sum())
# village_claims = village_claims.astype({'KHASRA': int})
village_claims['KHASRA'].dropna(inplace = True)
# df_repeated = .loc[df.index.repeat(2)]

# print(village['Village'])

plt.show()

village_claims.to_file('nagla_dhanoua.shp', driver="ESRI Shapefile")
