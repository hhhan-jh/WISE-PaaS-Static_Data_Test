# 🏗️ WISE-PaaS 기반 산업 현장 충돌 위험 모니터링 시스템

## 📖 프로젝트 개요
이 프로젝트는 산업 현장(공장, 물류센터 등)에서 작업자와 지게차 간의 **충돌 위험을 실시간으로 감지하고 시각화**하기 위한 미들웨어 및 모니터링 시스템입니다.

가상의 위치 데이터를 생성하여 **Python Flask 서버**를 통해 전송하고, **ngrok**을 거쳐 **WISE-PaaS(Grafana)** 대시보드에서 **히트맵(Heatmap)**과 **안전 점수(Safety Score)** 형태로 시각화합니다.

---

## 📌 주요 기능
1. **가상 데이터 생성 (Dummy Data Generator)**
   - 작업자와 지게차의 이동 경로를 시뮬레이션하여 위치 좌표(x, y) 및 거리(distance) 데이터 생성
   - 특정 반경(3m) 이내 진입 시 충돌 위험 로그 생성
2. **SimpleJson 호환 미들웨어 서버 (Flask)**
   - WISE-PaaS의 SimpleJson Datasource 규격에 맞춘 REST API 제공
   - **다중 타겟(Multi-target) 지원:** x, y 좌표 및 거리 데이터를 동시에 처리
   - **시간 필터링(Time Filtering):** 대시보드 요청 시간 범위에 따른 정확한 데이터 슬라이싱
3. **데이터 시각화 (WISE-PaaS/Grafana)**
   - **위험 구역 히트맵 (Echarts):** 충돌 위험이 감지된 위치를 산점도(Scatter Plot)와 밀도(Density) 기반 붉은 점으로 시각화
   - **안전 점수판 (Singlestat):** 특정 시간(예: 최근 30분) 동안 발생한 위험 횟수를 집계하여 '안전/관심/주의/위험/심각' 5단계 상태 표시

---

## 🛠 기술 스택 (Tech Stack)
- **Language:** Python 3.x
- **Framework:** Flask (Web Server), Flask-CORS
- **Tunneling:** ngrok (Localhost 외부 노출)
- **Visualization:** WISE-PaaS (Based on Grafana), Echarts (JavaScript)
- **Data Format:** JSON

---

## 📂 프로젝트 구조
```bash
📦 Project-Root
 ┣ 📂 server                 # SimpleJson 규격의 미들웨어 서버 코드, 시뮬레이션 데이터 저장
 ┣ 📂 dashboard              # 대시보드 관련 코드 저장
 ┣ 📜 generate_data.py       # 충돌 시나리오 더미 데이터 생성기
 ┗ 📜 README.md              # 프로젝트 설명서
```
---
## 🚀 실행 방법 (Getting Started)

### 1. 환경 설정 및 설치
```bash
# 필수 라이브러리 설치
pip install flask flask-cors
```
### 2. 더미 데이터 생성
```
# 데이터 생성 스크립트 실행 (예시)
python generate_data.py
# 실행 후 dummy_data_1hour.json 파일이 생성되었는지 확인
```
### 3. 서버 실행
```
python server.py
# 기본 포트: 5001 (MacOS AirPlay 충돌 방지)
```
### 4. 외부 접속 허용 (ngrok)
WISE-PaaS 클라우드에서 로컬 서버에 접속하기 위해 터널링을 수행합니다.
```
ngrok http 5001
```
실행 후 생성된 https://xxxx.ngrok-free.app 주소를 복사합니다.

---
## 📊 WISE-PaaS 대시보드 설정 가이드
### 1. Data Source 연결
* Type: SimpleJson
* URL: ngrok에서 생성된 HTTPS 주소 입력 (예: https://abcd-1234.ngrok-free.app)

### 2. 패널 설정: 위험 구역 히트맵 (Heatmap)
* Panel Type: Echarts
* Metrics: x, y 타겟 선택
* Visualization Code (JavaScript): heatmap.js 참고

### 3. 패널 설정: 안전 점수판 (Scoreboard)
* Panel Type: Singlestat
* Metric: distance
* Stat: Count (개수 집계)
* Thresholds: 0~, 50~, 100~, 150~, 200~ (green → yellow → Orange → Red → purple)
* Coloring: Background 체크

---
## 💻 WISE-PaaS 대시보드 스크린샷
<img width="1822" height="1180" alt="스크린샷 2025-11-21 오후 7 27 49" src="https://github.com/user-attachments/assets/c61adabc-f0e4-4388-95e7-d6c40167a20a" />

