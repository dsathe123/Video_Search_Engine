#%%
import os
import zmq
import sys
import uuid
import pickle
import yaml
#%%
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")
video_metadata = yaml.safe_load(open("config/video_metadata.yml"))


# sys.argv = ["", "data/Queries/Videos/video6_1.mp4", "data/Queries/Audios/video6_1.wav"]
# sys.argv = ["", "data/testing/clip_vid.mp4", "data/testing/clip_vid.wav"]
if len(sys.argv) == 1:
    print("Quit")
    socket.send(pickle.dumps("quit"))
    sys.exit(0)

#%%
assert len(sys.argv) == 3, f"Usage python <name>.py <query-video-path>.mp4 <query-audio-path>.wav"
query_video_path = sys.argv[1]
query_audio_path = sys.argv[2]

#%%
input_data = dict(
    id=uuid.uuid4().hex,
    query_video_path=query_video_path,
    query_audio_path=query_audio_path
)
#%%
socket.send(pickle.dumps(input_data))
#%%
result = pickle.loads(socket.recv())
print('Video Name: ', result['media_id'])
print('Frame: ', result['frame'])
# #%%
# video_name = f"{os.path.basename(result['audio_result'][0][0][2])}.mp4"
# video_path = os.path.join("data\Videos", video_name)
# time = result['audio_result'][0][0][3]
# #%%
import sys
sys.path.append("src")
from player.media_player import play_video_from
from player.media_player_mac import play_video_from

#%%
video_path = os.path.join("data", "Videos", result['media_id'] + ".mp4")
position = result["media_player_time"]
# play_video_from(video_path, position)
# print(video_metadata[result['media_id']]['total_length'], str(result['time']) + '.0')
play_video_from(video_path, str(result['time']) + '.0', video_metadata[result['media_id']]['total_length'])
#%%