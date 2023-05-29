from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
import tkinter as tk
import pytube, os

def new_window(title='YTDL (GUI Version 2)'): window = tk.Tk() ; window.title(title) ; return window
def message_window(text, text_colour='white'): window = new_window() ; grid(label(window, text, text_colour), 0, 0) ; grid(button(window, window.destroy, 'Continue'), 0, 1) ; window.mainloop()
def grid(widget, column, row, pady=10, padx=10, columnspan=1, rowspan=1): exec('widget.grid(column={}, row={}, pady={}, padx={}, columnspan={}, rowspan={})'.format(column, row, pady, padx, columnspan, rowspan))
def frame(master): return tk.Frame(master=master)
def label(master, text, text_colour='white'): return tk.Label(master=master, text=text, fg=text_colour)
def button(master, command, text, text_colour='black'): return tk.Button(master=master, text=text, fg=text_colour, command=command)
def radio_button(master, text, variable, value): exec('global variable') ; return tk.Radiobutton(master=master, text=text, variable=variable, value=value)

def download_single_main_code(url_obj, file_type, file_extension):
    def refresh_dl_window(master, label_obj): label_obj.config(text='Downloaded') ; grid(button(master, window.destroy, 'Ok'), 0, 1)

    cleaned_filename = url_obj.title
    for char in banned_chars: cleaned_filename = cleaned_filename.replace(char, banned_char_replace_with)
    filename = cleaned_filename + file_extension

    if file_type == 'audio': stream_itag = 140
    if file_type == 'video': stream_itag = 18

    window = new_window()
    filename_text = label(window, filename) ; grid(filename_text, 0, 0)
    buttons_grid = frame(window) ; grid(buttons_grid, 0, 1)
    continue_button = button(buttons_grid, window.destroy, 'Download') ; grid(continue_button, 0, 0)
    quit_button = button(buttons_grid, quit, 'Quit') ; grid(quit_button, 1, 0)
    window.mainloop()

    window = new_window()
    text = label(window, 'Downloading...') ; grid(text, 0, 0, 20, 20)
    window.after(1, lambda:url_obj.streams.get_by_itag(stream_itag).download(dl_path, filename, max_retries=2))
    window.after(1, lambda:refresh_dl_window(window, text))
    window.mainloop()

def download_single():
    window = new_window()
    url_frame = frame(window) ; grid(url_frame, 0, 0)
    url_txt = label(url_frame, 'URL:') ; grid(url_txt, 0, 0, pady=0)
    url_StringVar = tk.StringVar(value=None)
    url_input = tk.Entry(master=url_frame, textvariable=url_StringVar) ; grid(url_input, 1, 0, pady=0)
    aov_frame = frame(window) ; grid(aov_frame, 0, 1)
    audio_or_video_StringVar = tk.StringVar(value=None)
    audio_radio = radio_button(aov_frame, 'Audio', audio_or_video_StringVar, 'audio') ; grid(audio_radio, 0, 0, pady=0)
    video_radio = radio_button(aov_frame, 'Video', audio_or_video_StringVar, 'video') ; grid(video_radio, 1, 0, pady=0)
    start_button = button(window, window.destroy, 'Start') ; grid(start_button, 0, 2)
    window.mainloop()

    audio_or_video = audio_or_video_StringVar.get()
    pyt_url = pytube.YouTube(url_StringVar.get())

    if audio_or_video == 'audio': download_single_main_code(pyt_url, 'audio', '.mp3')
    if audio_or_video == 'video': download_single_main_code(pyt_url, 'video', '.mp4')

banned_chars = ['*', "'", '"', '/', '|', ';', '`', '%', '#', '\\', '@', '[', ']']
banned_char_replace_with = ''

window = new_window()
grid(label(window, 'I have the latest version of the Chrome browser installed.', 'red'), 0, 0, 2, 10)
grid(label(window, 'I have choosen a public or unlisted video or playlist.', 'red'), 0, 1, 2, 10)
button_frame = frame(window) ; grid(button_frame, 0, 2, 5, 0)
grid(button(button_frame, window.destroy, 'Agree'), 0, 0, 5, 5)
grid(button(button_frame, quit, 'Quit'), 1, 0, 5, 5)
window.mainloop()

window = new_window()
input_frame = frame(window) ; grid(input_frame, 0, 0)
grid(label(input_frame, 'Download path:'), 0, 0, pady=0)
dl_path = tk.StringVar(value=f'/Users/{os.environ.get("LOGNAME")}/Desktop/ytdl_downloaded')
grid(tk.Entry(master=input_frame, textvariable=dl_path), 1, 0)
grid(button(window, window.destroy, 'Continue'), 0, 1)
window.mainloop()
dl_path = dl_path.get()

single_or_playlist = 'Not selected'
window = new_window()
grid(button(window, lambda:exec('global single_or_playlist ; single_or_playlist = "single" ; window.destroy()'), 'Single Video'), 0, 0)
grid(button(window, lambda:exec('global single_or_playlist ; single_or_playlist = "playlist" ; window.destroy()'), 'Playlist'), 1, 0)
window.mainloop()

if single_or_playlist == 'single': download_single()
if single_or_playlist == 'playlist':
    def download_all(videos):
        window = new_window()
        grid(label(window, f'{len(videos)} Videos', 'yellow'), 0, 0, pady=0)
        titles_frame = tk.Frame(window, height=100) ; grid(titles_frame, 0, 1, pady=0)
        canvas = tk.Canvas(master=titles_frame, width=400) ; canvas.grid(column=0, row=0, sticky="nsew")
        for video in videos: canvas.create_window(0, videos.index(video)*19, anchor='nw', window=tk.Label(master=canvas, text=video['title']), height=20)
        vertical_scrollbar = tk.Scrollbar(master=window, orient='vertical', command=canvas.yview, width=15, bg='black') ; vertical_scrollbar.grid(column=1, row=1, sticky="nsew")
        horizontal_scrollbar = tk.Scrollbar(master=window, orient='horizontal', command=canvas.xview, width=10) ; horizontal_scrollbar.grid(column=0, row=2, sticky="nsew")
        canvas.configure(scrollregion=canvas.bbox('all'), yscrollcommand=vertical_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)
        audio_or_video_StringVar = tk.StringVar(value=None)
        aov_frame = frame(window) ; grid(aov_frame, 0, 3, pady=0)
        grid(radio_button(aov_frame, 'Audio', audio_or_video_StringVar, 'audio'), 0, 2, pady=0)
        grid(radio_button(aov_frame, 'Video', audio_or_video_StringVar, 'video'), 1, 2, pady=0)
        btn_frame = frame(window) ; grid(btn_frame, 0, 4)
        grid(button(btn_frame, window.destroy, 'Download'), 0, 0)
        grid(button(btn_frame, quit, 'Quit'), 1, 0)
        window.mainloop()

        def dl(window_obj, videos):
            if audio_or_video_StringVar.get() == 'audio':
                for video in videos:
                    try: pytube.YouTube(video['url']).streams.get_by_itag(140).download(output_path=dl_path, filename=video['title']+'.mp3', max_retries=2)
                    except Exception: print(f'Error: {video["title"]} ({video["url"]})')
            if audio_or_video_StringVar.get() == 'video':
                for video in videos:
                    try: pytube.YouTube(video['url']).streams.get_by_itag(18).download(output_path=dl_path, filename=video['title']+'.mp4', max_retries=2)
                    except Exception: print(f'Error: {video["title"]} ({video["url"]})')
            window_obj.destroy()

        window = new_window()
        grid(label(window, f'Downloading ...'), 0, 0)
        window.after(1, lambda:dl(window, videos))
        window.mainloop()

        window = new_window()
        grid(label(window, 'Finished'), 0, 0)
        grid(button(window, quit, 'Quit'), 0, 1)
        window.mainloop()

    def download_seperate(videos):
        def assign(variable, value): variable['dl_type'] = value
        def make_row(row_index):
            tk.Label(master=videos_frame, text=row_index-1).grid(column=0, row=row_index)
            tk.Label(master=videos_frame, text=video['title']).grid(column=1, row=row_index)
            btn_audio = tk.Button(master=videos_frame, text='Audio', command=lambda video=video:[assign(video, 'audio'), btn_video.config(fg='white'), btn_audio.config(fg='green')]) ; btn_audio.grid(column=2, row=row_index, padx=2)
            btn_video = tk.Button(master=videos_frame, text='Video', command=lambda video=video:[assign(video, 'video'), btn_video.config(fg='green'), btn_audio.config(fg='white')]) ; btn_video.grid(column=3, row=row_index, padx=2)
        def dl(window_obj, videos):
            for video in videos:
                if video['dl_type'] == 'audio': pytube.YouTube(video['url']).streams.get_by_itag(140).download(output_path=dl_path, filename=video['title']+'.mp3', max_retries=2)
                if video['dl_type'] == 'video': pytube.YouTube(video['url']).streams.get_by_itag(18).download(output_path=dl_path, filename=video['title']+'.mp4', max_retries=2)
            window_obj.destroy()

        window = new_window()
        headers_frame = tk.Frame(master=window) ; grid(headers_frame, 0, 0)
        grid(tk.Label(master=headers_frame, text=f'{len(videos)} videos total', fg='yellow'), 0, 0, 0, 0, 4)
        grid(tk.Label(master=headers_frame, text='Video', fg='red'), 0, 1, 0, 0)
        grid(tk.Label(master=headers_frame, text='Video Title', fg='red'), 1, 1, 0, 0)
        grid(tk.Label(master=headers_frame, text='Download Type', fg='red'), 2, 1, 0, 0, 2)
        videos_frame = frame(window) ; grid(videos_frame, 0, 1)
        row = 2
        for video in videos: make_row(row) ; row += 1
        grid(tk.Button(master=window, text='Start', command=window.destroy), 0, 4, 4)
        window.mainloop()

        window = new_window()
        grid(label(window, f'Downloading...'), 0, 0)
        window.after(1, lambda:dl(window, videos))
        window.mainloop()

        window = new_window()
        grid(label(window, 'Finished'), 0, 0)
        grid(button(window, quit, 'Quit'), 0, 1)
        window.mainloop()

    message_window('A chrome window will open. Once it has opened, please return here.\n(The program may freeze while it downloads the required files; Please be patient, chrome will launch when finished)')

    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get('https://www.youtube.com')

    message_window('Please go to the browser and select your cookie preferences, then navigate to the playlist and then press continue below.')
    message_window('If the playlist has more than 100 videos, please scroll down to the end of the playlist so that they load and then press continue below.')

    sleep(1) ; raw_source = driver.page_source ; driver.quit()
    source = BeautifulSoup(raw_source, 'html.parser')
    videos_raw = source.find_all('div',{'id': 'container', 'class': 'style-scope ytd-playlist-video-renderer'})
    videos = []
    for video in videos_raw:
        raw_title = video.find('a', {'id': 'video-title'})
        cleaned_title = raw_title.text.replace('\n          ', '').replace('\n        ', '').replace(' ', '', 0)
        for char in banned_chars: cleaned_title = cleaned_title.replace(char, banned_char_replace_with)
        url = 'https://youtube.com' + video.find('a', {'id': 'video-title'})['href']
        videos.append({'title':cleaned_title, 'url':url, 'dl_type':'not_selected'})

    window = new_window()
    grid(label(window, 'Select video download type selection'), 0, 0)
    all_or_seperate = 'Not selected'
    button_frame = frame(window) ; grid(button_frame, 0, 1)
    grid(button(button_frame, lambda:exec('global all_or_seperate ; all_or_seperate = "all" ; window.destroy()'), 'All'), 0, 0)
    grid(button(button_frame, lambda:exec('global all_or_seperate ; all_or_seperate = "seperate" ; window.destroy()'), 'Individual'), 1, 0)
    window.mainloop()

    if all_or_seperate == 'all': download_all(videos)
    if all_or_seperate == 'seperate': download_seperate(videos)