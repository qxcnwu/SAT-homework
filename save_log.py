import numpy as np
from mine_clearance import mine,position

def save_log(M:mine,save_path):
    """
    保存中途文件
    """
    np.save(save_path,np.stack(M.showlabel_list,axis=2))
    listx=[[pos.x,pos.y] for pos in M.position_list]
    np.save(save_path+"2",np.array(listx))
    return

def load_log(save_path):
    """
    读取log文件
    """
    show_list=np.load(save_path,allow_pickle=True)
    position_list=np.load(save_path.replace(".npy","2.npy"),allow_pickle=True)
    return show_list,position_list