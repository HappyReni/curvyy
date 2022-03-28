# curvyy
### *A handwriting classifier based on EMNIST image set*


![hello](https://user-images.githubusercontent.com/74769597/160383052-2665f4ea-b36f-424e-b70f-a6ac6f72c9fd.gif)

## Purpose

손으로 쓰인 문자를 숫자와 알파벳 소문자, 대문자로 인식하고 분류하는 프로그램을 만든다

## Plan

1. EMNIST 이미지 셋을 활용하여 CNN 신경망을 학습한다.
2. 손글씨를 쓸 수 있는 Python GUI 프로그램을 PyQt로 구현한다.
3. 학습한 모델에 직접 그린 손글씨를 입력하여 무슨 글자인지 인식한다.

## Usage

 왼쪽의 캔버스에 문자를 그리면 신호등의 노란색 불이 들어온다. 
 
 노란색 불이 켜져있다면 계속해서 캔버스에 그릴 수 있다.
 
 그리는 것을 멈추면 잠시 후 초록색 불로 바뀌고 우측 텍스트 박스에 인식한 글자가 나타난다.
 

## Technologies

* Python
* PyQt5
* numpy
* pandas
* tensorflow
* keras

## Reference
* https://wikidocs.net/book/2165 - PyQt5 튜토리얼
* https://www.kaggle.com/code/achintyatripathi/emnist-letter-dataset-97-9-acc-val-acc-91-78 - EMNIST CNN 학습 커널
