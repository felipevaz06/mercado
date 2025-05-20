from pipelines.transform_data import transform_data
from pipelines.load_to_mongodb import save_to_mongodb, test_connection



paguemenos = 'results/paguemenos/'
saovicente = 'results/saovicente/'


transformed_data = transform_data([paguemenos, saovicente])
save_to_mongodb(transformed_data)