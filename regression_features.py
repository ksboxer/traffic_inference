
import itertools



def generate_features_from_configs(configs):
	feature_list = []
	for featureset in configs['featureset']:
		#print(configs['featureset'][featureset])
		temp_feature_list = configs['featureset'][featureset]
		#feature_list.append(temp_feature_list)
		temp_list = []
		for i in xrange(1,len(temp_feature_list)+1):
			ex = [list(x) for x in itertools.combinations(temp_feature_list, i)]
			temp_list = temp_list + ex
			for curr in feature_list:
				for e in ex:
					merged_list = curr + e
					temp_list.append(merged_list)
			#temp_list= temp_list + ex
		feature_list = feature_list + temp_list
	return feature_list