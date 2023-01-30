# twofastgif


## 개발 동기 및 앱 설명
  twofastgif는 기존의 video to GIF 웹 어플리케이션들이 한번에 한개의
  GIF 변환만을 제공하는 불편함을 개선하기 위한 웹 어플리케이션이다.
  
  다른 GIF변환 웹 어플리케이션들의 불편함을 개선하여 동시에 2개의 비디오를 고화질의 GIF형식으로 변환할 수 있다.
  비디오파일을 직접 지정하여 변환할 수도 있지만 비디오 URL을 복사하여 변환 가능하다.
  
## 사용 예시
  1. 변환할 동영상 어플리케이션에 드래그앤드랍 or 파일 찾아서 넣기
  
  ![넣기](https://user-images.githubusercontent.com/52123195/134807085-90893491-824a-43aa-bad8-acbd7ec98606.gif)
  
  2. 변환되어 나올 GIF 옵션 고르기
  
  ![업션](https://user-images.githubusercontent.com/52123195/134807144-fb1495aa-2bb1-4a1b-97a5-f5cf66a74555.gif)
  
  3. 변환하기

  ![변환](https://user-images.githubusercontent.com/52123195/134807238-4cea92fc-e25b-40a9-b744-807aefb2d39d.gif)

  (동영상 URL도 같은형식으로 진행한다)
  
  ![url](https://user-images.githubusercontent.com/52123195/134807350-2cf41927-c10e-4a79-b2fd-edb0c31fd34c.png)
  
  
## 앱 제작
  백엔드, AWS - 장민혁(jeongbalmount)
  
   1. 웹 프레임워크 - Python Django
    
   <img width="487" alt="djangoMTV" src="https://user-images.githubusercontent.com/52123195/134920751-45f71c08-f4b9-429e-b17b-97e25fb79f42.png">
   
    twofastgif는 웹사이트를 매개로 서비스를 제공하기 때문에 
    Python 웹프레임워크인 Django를 사용하였다.
    Django는 MVC구조로 되어 있지만 명칭이 다르다.(Model -> Model, Controller -> View, View -> Template)
    
    1. twofastgif.com을 통해 동영상 파일을 Post로 서버 전송한다.
    2. 유효성 검사를 통해 정상적인 동영상 파일 혹은 동영상 URL인지 확인하고
    Model에 저장 요청을 한다.
    3. 동영상을 AWS S3에 저장한다.
    4. S3에 저장된 동영상의 URL을 GIF변환 모듈에 전달한다.
    5. 동영상을 GIF로 변환하고 S3에 저장한다.
    6. S3에 저장된 GIF의 URL을 전달한다.
    7. 웹에 static file들과 GIF의 URL들을 전달한다.
    
    정상적인 동영상과 동영상 URL을 서버가 받아들이는지 확인하는 작업이 쉽지 않았다.
    많은 시행착오 끝에 동영상은 mime타입을 확인하는 내장 함수를 통해 변환이 가능한지 확인하였고,
    동영상 URL에선 ffProbe 라이브러리를 통해 URL을 검증하고 동영상을 불러왔다.
    
    각각의 GIF 변환 옵션은 조건문을 통해 유효성 검사를 실시하였다.
    서버로 넘어온 각 옵션이 정수형, 문자형등 유효한 형식임을 Modelform을 통해 검증하는것 뿐만 아니라
    원하는 GIF 변환 시간이 15초를 넘기지 않거나 fps 값이 정해진 값 이외의 값인지 같은
    세세한 옵션 값까지 따져야 했기 때문이다.
   
   2. DB - sqlite 
   
    처음에는 AWS RDS를 사용했지만 동영상과 GIF의 URL, 그리고 GIF변환과 관련된
    옵션 값만을 저장하면 되기 때문에 내장된 sqlite를 사용하여 효율을 늘렸다.
    
   3. 클라우드 - AWS(EC2, ELB)
     
   ![aws](https://user-images.githubusercontent.com/52123195/135215559-bd961344-8091-48f1-90fd-66b82f61287f.png)
     
    AWS 클라우드를 이용하여 웹 어플리케이션 서비스를 제공하였다.
    처음 서비스를 구상하였을때는 EC2 컴퓨터에 웹서버를 올려 앱을 구동하려 했다.
    
    하지만 동영상을 GIF로 변환하는 과정이 가벼운 프로세싱이 아니기 때문에
    ELB를 통해 스케일 아웃하는 방법을 채택하였다. ELB를 통해 EC2를 연결하고
    각 컴퓨터 헬스체크 및 사용자 증감에 따라 연결 컴퓨터 수를 자동으로 조절한다.
    
   5. 웹서버 - nginx, Gunicorn
    
    웹서버는 nginx를 사용하였고 서비스 지속 실행을 위한 wsgi는 Gunicorn을 
    사용하였다.
    
    Load balancer를 사용하기 때문에 직접적으로 웹서버에서 https를 다루는 것이 아닌
    ELB에서 https 리디렉션을 담당한다.
  
  프론트엔드(JS, vue, css, html) - 박상민(https://sangmin802.github.io/about/) 
    
    바닐라 JS사용, vue와 vue pre-render 사용, css와 html디자인

  

