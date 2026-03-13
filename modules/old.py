# @staticmethod
# def reconstruct_TP(gamma_dict:dict,source_id:int=0):
#     """
#     reconstruct temporal paths from gamma_dict
#     Input:
#         gamma_dict
#             key=node_id
#             value=(reachability,visited_time,predecessor_id,predecessor_visited_time)
#         source_id
#     Output:
#         TP_dict

#         target node별 temporal path를 재구성해서 transform 해야하는 이유: a->b->c 의 경우, a->b에 대한 변환과 a->b->c에 대한 변환 모두 수행해야 하기 때문. 
#         b에 10, c에 20에 도달 하였는데 interval이 20인 경우, b에도 도달 가능하다는 정보를 잃지 않기 위해서 a->b_20과 a->c_20 모두 생성해야 한다.
#     """
#     path_dict={}
#     for node in gamma_dict.keys():
#         path_list=[]
#         target=node
#         while True:
#             if target==source_id:
#                 break
#             predecessor=gamma_dict[target][2]
#             visited_t=gamma_dict[target][1]
#             edge_event=(predecessor,target,visited_t)
#             path_list.append(edge_event)
#             target=predecessor
#         path_dict[node]=list(reversed(path_list))