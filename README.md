#YouTube Songs Downloader (🇰🇷 소개)

이 프로젝트는 PyQt5를 사용하여 유튜브에서 노래를 검색하고 다운로드할 수 있는 GUI 애플리케이션입니다. 사용자는 원하는 노래 제목을 입력하고, 다운로드 경로를 설정한 후, 버튼을 클릭하여 손쉽게 음악을 mp4 형식으로 다운로드할 수 있습니다.

🛠 주요 기능

유튜브 검색: 노래 제목을 기반으로 유튜브에서 첫 번째 영상을 자동 검색합니다.

다운로드: 선택된 경로에 해당 영상을 mp4 형식으로 저장합니다.

GUI: PyQt5 기반의 직관적인 사용자 인터페이스

비동기 처리: 다운로드 중에도 프로그램이 멈추지 않도록 QThread 사용

📦 사용한 라이브러리

PyQt5: GUI 구축

pytubefix: YouTube 영상 다운로드

yt_dlp: 유튜브 검색 (ytsearch)

tkinter.messagebox: 오류 및 경고 메시지 표시

🧩 프로그램 구성

MyWindow: 메인 윈도우 클래스

노래 추가

경로 입력

다운로드 버튼 및 로그

리스트 위젯을 통해 추가된 노래 확인 가능

DownloadWorker (QThread 상속)

run(): 각 노래를 검색하고 다운로드 수행

get_top_video_url(): yt_dlp를 활용해 유튜브에서 검색

download_youtube_video_mp4(): pytubefix로 영상 다운로드

#YouTube Songs Downloader (English)

This project is a GUI application built with PyQt5 that allows users to search and download YouTube songs as mp4 files. Users simply enter a song title and download location, and the application handles the rest.

🛠 Features

YouTube Search: Automatically finds the top result for the entered song title.

Video Download: Saves the video in mp4 format to the specified location.

GUI: User-friendly interface built with PyQt5

Threading: Uses QThread to prevent UI freezing during downloads

📦 Libraries Used

PyQt5: For GUI elements

pytubefix: For downloading YouTube videos

yt_dlp: For searching YouTube using ytsearch

tkinter.messagebox: For displaying errors and alerts

🧩 Structure

MyWindow: The main window class

Input field for song titles

Input field for download path

Add to list button

Download button

Log label and song list widget

DownloadWorker (inherits QThread)

run(): Searches and downloads each song

get_top_video_url(): Finds the top video using yt_dlp

download_youtube_video_mp4(): Downloads the video using pytubefix

💡 추가 정보 / More Info

다운로드가 진행 중일 때도 UI가 멈추지 않음 (QThread 덕분)

잘못된 입력이나 오류 발생 시 tkinter의 메시지박스로 즉시 알림

다중 노래 지원

🔒 주의사항 / Caution

이 프로젝트는 교육 및 개인용도로만 사용해야 합니다.

저작권이 있는 콘텐츠를 무단으로 다운로드하지 마세요.


