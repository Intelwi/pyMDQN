import torch
import torchvision.transforms as T
import numpy as np
from PIL import Image
from pathlib import Path
import copy
from TrainNQL import TrainNQL



device = "gpu"#torch.device("cuda" if torch.cuda.is_available() else "cpu")



def main():	
	torch.manual_seed(torch.initial_seed())  
	episode=torch.load('files/episode.dat')

	agent=TrainNQL(epi=episode)

	target_net=4
	agent.load_data()
	for j in range(50):
		print("\nTrain= "+str(j+1)+"/50")
		for i in range(10):
			print("epoch ",i+1)
			agent.train()
		agent.gray_target_net=copy.deepcopy(agent.gray_policy_net)
		agent.depth_target_net=copy.deepcopy(agent.depth_policy_net)	


	gray_policy_net=copy.deepcopy(agent.gray_policy_net)
	depth_policy_net=copy.deepcopy(agent.depth_policy_net)

	if episode%target_net==1:
		agent.gray_target_net=copy.deepcopy(agent.gray_policy_net)
		agent.depth_target_net=copy.deepcopy(agent.depth_policy_net)

	gray_target_net = copy.deepcopy(agent.gray_target_net)
	depth_target_net = copy.deepcopy(agent.depth_target_net)

	model_dir='results/ep'+str(episode)

	Path(model_dir).mkdir(parents=True, exist_ok=True)

	save_gray_policy_net=model_dir+'/modelGray.net'
	save_gray_target_net=model_dir+'/tModelGray.net'
	save_depth_policy_net=model_dir+'/modelDepth.net'
	save_depth_target_net=model_dir+'/tModelDepth.net'

	torch.save(gray_policy_net,save_gray_policy_net)
	torch.save(gray_target_net,save_gray_target_net)
	torch.save(depth_policy_net,save_depth_policy_net)
	torch.save(depth_target_net,save_depth_target_net) 

	episode=episode+1
	print("Episode: ",episode)
	torch.save(episode,'files/episode.dat')
	with open('files/episode.txt', 'w') as f:
		f.write(str(episode))	

if __name__ == "__main__":
   main()