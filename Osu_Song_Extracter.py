import tkinter as tk
from tkinter import filedialog
import os
import shutil

def Count_Folders(self):
    folder_list = Read_Files(self, self.songs_location)
    self.instruction.config(text = "안내: 검색된 폴더 개수는 {}개 입니다.".format(len(folder_list)))

def Read_Files(self, dir):
    file_list = os.listdir(dir)
    return file_list

def Ask_Directory(self):
    dirName = filedialog.askdirectory()
    return dirName

def Activate_Extract_Button_Condition_Check(self):
    # print("체크중")
    if self.songs_location != "" and self.extract_location != "":
        self.extract_start_btn.config(state = 'active')
        Count_Folders(self)  # 폴더 개수 세고, instruction label에 설명 해주기.
        # print("버튼활성화")
    else:
        self.extract_start_btn.config(state = 'disabled')
        self.instruction.config(text = "안내: Songs 경로와 노래가 저장될 경로를 선택해주세요.") 
        # print("버튼비활성화")


class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        
        self.title('Extract Osu Songs')              # 창 제목 설정
        self.geometry("500x250+250+700")   # 창 크기 (너비x높이+x좌표+y좌표)
        self.resizable(False, False)   # 창 크기 조절 여부        
        
        self._frame = None
        self.switch_frame(StartPage)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


class StartPage(tk.Frame):  

    def Select_Songs_Location(self):
        self.songs_location = Ask_Directory(self)
        self.songs_location_show.config(text="Songs Location : " + self.songs_location)
        Activate_Extract_Button_Condition_Check(self)

    def Select_Extract_Location(self):
        self.extract_location = Ask_Directory(self)
        self.extract_location_show.config(text="Extract Location : " + self.extract_location)
        Activate_Extract_Button_Condition_Check(self)

    def Extract_Start(self):
        print("시작\n")
        folder_list = Read_Files(self, self.songs_location) 

        for i in folder_list:
            try:
                inside_folder_location = self.songs_location + "/" + i  
                inside_files = Read_Files(self, inside_folder_location) # 폴더 내부의 모든 파일 이름을 스캔
                # print(inside_files)
                # print(inside_folder_location)
                # print(self.extract_location)

                if inside_folder_location == self.extract_location:
                    print(i)
                    print("여긴 출력될 폴더인걸?\n")
                    continue

                collect_music_files = [] # 이 리스트에 음악 확장자인 녀석의 이름을 담는다.
                for j in inside_files:
                    if j[-3:] == "mp3" or j[-3:] == "MP3" or j[-3:] == "ogg" or j[-3:] =="wav" or j[-3:] == "flac":
                        # print("끝자리가" + j[-3:] + "라서 추가했다.")
                        collect_music_files.append(j)
                # print("뮤직 파일은 누구?", collect_music_files) 

                if len(collect_music_files) >= 2:
                    file_sizes = []
                    for k in collect_music_files: # 뮤직 확장자인 녀석이 다수일 수도 있기때문에 그 중 가장 용량이 큰 녀석만 복사
                        file_sizes.append(os.path.getsize(self.songs_location + "/" + i + "/" + k))
                    # print("뮤직 파일들의 용량들은 몇?", file_sizes)
                    # print("그 중 가장 용량이 큰 애는 몇?", max(file_sizes))
                    greatest_size_file = collect_music_files[file_sizes.index(max(file_sizes))]
                    # print("그 중 가장 큰 애는 누구?", greatest_size_file)
                    the_file_to_be_copied = greatest_size_file
                elif len(collect_music_files) == 0:
                    print(i)
                    print("너는 음악파일이 없네?\n")
                    continue
                else:
                    # print("너는 혼자구나")
                    the_file_to_be_copied = collect_music_files[0]

                the_file_to_be_copied_location = self.songs_location + "/" + i + "/" + the_file_to_be_copied    
                extension_name = the_file_to_be_copied[-4:]            
                new_file_name = i.split()
                del new_file_name[0]
                new_file_name = ' '.join(new_file_name)
                new_file_name = new_file_name + extension_name
                # print(new_file_name)
                new_file_directory = self.extract_location + "/" + new_file_name
                # print(new_file_directory)
                old_file_directory = self.extract_location + "/" + the_file_to_be_copied 
                # print(old_file_directory)

                if os.path.isfile(new_file_directory): # 저장하려는 곳에 이미 똑같은 이름의 파일이 있는경우                 
                    print(i)
                    if os.path.getsize(the_file_to_be_copied_location) > os.path.getsize(new_file_directory): # 두 개의 용량비교 해서 큰 쪽꺼를 가져온다.
                        os.remove(new_file_directory)
                        shutil.copy2(the_file_to_be_copied_location, self.extract_location) # 카피 실행
                        os.rename(old_file_directory, new_file_directory) # 이름변경 실행
                        print("이미 있는 녀석이지만 큰 용량의 것을 가져왔다.\n")
                    else:
                        print("이미 동일한 파일이 있으니 복사도 안하고 이름도 안바꿈.\n")
                        continue
                else:                        
                    shutil.copy2(the_file_to_be_copied_location, self.extract_location) # 카피 실행
                    # print(the_file_to_be_copied_location + "파일을" + self.extract_location + "로 카피했습니다.")
                    os.rename(old_file_directory, new_file_directory) # 이름변경 실행
                    # print("새로운 파일의 이름은 " + new_file_name + " 입니다.")
            except NotADirectoryError:
                print(i)
                print("이 친구는 폴더가 아니라 그냥 파일이네.\n")
                continue

        print("복사 완료\n")

    def __init__(self, master):  
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self, width = 500, height = 250)

        # Songs 위치, 저장 위치 초기화  
        self.songs_location = ""
        self.extract_location = ""

        #위에서부터 위젯 위치 순서대로 나열

        self.instruction = tk.Label(self, text = "안내: Songs 경로와 노래가 저장될 경로를 선택해주세요.") 
        self.instruction.place(x=25, y=15)
        
        self.songs_location_btn = tk.Button(self, text = 'Songs 경로 선택', anchor = 'center', command = self.Select_Songs_Location)
        self.songs_location_btn.place(x=25, y=50)    

        self.songs_location_show = tk.Label(self, text = "Songs Location :") 
        self.songs_location_show.place(x=25, y=80)
        
        self.extract_location_btn = tk.Button(self, text = '추출될 경로 선택', anchor = 'center', command = self.Select_Extract_Location)
        self.extract_location_btn.place(x=25, y=110)  

        self.extract_location_show = tk.Label(self, text = "Extract Location :")
        self.extract_location_show.place(x=25, y=140)

        self.extract_start_btn = tk.Button(self, text = '추출 시작', anchor = 'center', state = 'disabled', command = self.Extract_Start)
        self.extract_start_btn.place(x=25, y=195)  


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()