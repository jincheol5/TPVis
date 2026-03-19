# TPVis
Version: 1.0.0-alpha
현재 리뉴얼 중입니다.

# What is TPVis?
TPVis는 동적 네트워크에서의 ==시간적 정보 확산(temporal information diffusion)==을 직관적으로 분석할 수 있도록 지원하는 temporal path 시각화 시스템입니다.

기존 temporal graph 시각화 기법들은 temporal path를 표현하는 과정에서 visual misalignment, visual disconnection, time-constraint violation과 같은 시각적 혼란 요소들을 발생시켜 정보 흐름을 정확하게 파악하기 어렵다는 한계가 있습니다.

TPVis는 이러한 문제를 해결하기 위해:
- temporal path를 계산하고
- path-to-tree 변환 기법을 통해 tree 형태로 변환하며
- 이를 timeline 기반 레이아웃으로 시각화하여 시각적 혼란 요소들을 100% 제거합니다.

# How to use?
1. UI접속 및 TPVis engine 실행
    - [UI](https://jincheol5.github.io/TPVis/)
    - TPVis engine: `python -m app.run_tpvis_engine`

2. 데이터셋 업로드

3. 사용자 쿼리
 


# Paper Publication
Jincheol Oh, Haifa Gaza, Eunsol Gang, Jaewook Byun, "TPVis: A Temporal Path Visualization System for Intuitive Understanding of Information Diffusion Inside Temporal Networks." IEEE Access (2025) [Paper Link](https://doi.org/10.1109/ACCESS.2025.3586044).
