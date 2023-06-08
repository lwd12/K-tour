K-tour
=============
A website that enables searching and provides information about traditional Korean restaurants, accommodations, and recreational activities.


## Function   
> Naver popular elements API output      
> Use the National Traditional Restaurant API.   
> Use the National Traditional Accommodation API.   
> Use the National Traditional Festival API.   

## Img  
<img src="/search.png" width="70%" height="40%" title="px(픽셀) 크기 설정" alt="login"></img></br>


* Integrate Naver's popular list and search system where clicking on a name leads to the map API and marker creation.
```python
filename1 = "tour_craft.csv" # 파일 이름
acc = []
with open(filename1, "r", encoding="utf-8-sig") as csvfile:  # 공방 정보
    reader = csv.DictReader(csvfile)
    for row in reader:
        data = {row["FCLTY_NM"]: [row["RDNMADR_NM"]]}
        craft.append(data)


def translate(data_name):
	felist = []
  fevallist = []
	for d in festival:
	        for key, value in d.items():
	            for i in value:
	                if data_name in i:
	                    felist.append(key)
	                    fevallist.append(value)
return (
        felist,
        feval,)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method != "POST":
        acd = "전통숙소"
        fdd = "전통음식"
        spd = "문화관광지"
        accom = getdata(acd)
        food = getdata(fdd)
        spot = getdata(spd)
        return render_template(
            "index.html",
            accom=accom[0],
            food=food[0],
            spot=spot[0],
            basicafd=food[1],
            basicasp=spot[1],
            basicacc=accom[1],
        )
    else:
        data_name = request.form["area"]
        print(data_name)
        result = translate(data_name)
        # resultk = trans(data_name)
        con_name = request.form["con"]
        if con_name == "숙소":
            resultv = set(result[10])
            resultv = list(resultv)
            resultk = set(result[9])
            resultk = list(resultk)
            resultk.sort()
            resultv.sort()
        elif con_name == "식당":
            resultv = set(result[7])
            resultv = list(resultv)
            resultk = set(result[6])
            resultk = list(resultk)
            resultk.sort()
            resultv.sort()

        elif con_name == "축제":
            resultv = set(result[1])
            resultv = list(resultv)
            resultk = set(result[0])
            resultk = list(resultk)
            resultk.sort()
            resultv.sort()

        elif con_name == "놀거리":
            resultv = set(result[4])
            resultv = list(resultv)
            resultk = set(result[3])
            resultk = list(resultk)
            resultk.sort()
            resultv.sort()

        return render_template(
            "search.html",
            search=resultk,
            resultv=resultv,
        )
```


<img src="/marker.png" width="30%" height="30%" title="px(픽셀) 크기 설정" alt="setting"></img></br>

```python
//검색한 주소의 정보를 insertAddress 함수로 넘겨준다.
                    function searchAddressToCoordinate(address) {
                        naver.maps.Service.geocode({
                            query: address
                        }, function(status, response) {
                            if (status === naver.maps.Service.Status.ERROR) {
                                return alert('Something Wrong!');
                            }
                            if (response.v2.meta.totalCount === 0) {
                                return alert('올바른 주소를 입력해주세요.');
                            }
                            var htmlAddresses = [],
                                item = response.v2.addresses[0],
                                point = new naver.maps.Point(item.x, item.y);
    
    
                            insertAddress(item.roadAddress, item.x, item.y);
                            
                        });
                    }
                                        // 지도를 이동하게 해주는 함수
                    function moveMap(len, lat) {
                        var mapOptions = {
                                center: new naver.maps.LatLng(len, lat),
                                zoom: 18,
                                mapTypeControl: true
                            };
                        var map = new naver.maps.Map('map', mapOptions);
                        var marker = new naver.maps.Marker({
                            position: new naver.maps.LatLng(len, lat),
                            map: map
                        });
                    }
                    function createClickHandler(test) {
                        return function() {
                            searchAddressToCoordinate(test);
                        };
                    }
                    
    
                    var cardTextElements = document.getElementsByClassName("card-text1");

                    var LocalElements = document.getElementsByClassName("hide1");

                    
                    
                    // card-text 클래스를 가진 모든 요소에 클릭 이벤트 리스너를 추가합니다.
                    for (var i = 0; i < cardTextElements.length; i++) {
                        var test = LocalElements[i].innerText;
                        cardTextElements[i].addEventListener("click", createClickHandler(test));
                        };
```

<img src="/marker-1.png" width="30%" height="30%" title="px(픽셀) 크기 설정" alt="shadow"></img></br>


* Retrieve local information when a marker is clicked.
```python
    //검색정보를 테이블로 작성해주고, 지도에 마커를 찍어준다.
                    function insertAddress(address, latitude, longitude) {

                        var map = new naver.maps.Map('map', {
                            center: new naver.maps.LatLng(longitude, latitude),
                            zoom: 14
                        });
                        var marker = new naver.maps.Marker({
                            map: map,
                            position: new naver.maps.LatLng(longitude, latitude),
                        });


                        var contentString = [
                            '<div class="iw_inner">',
                            '   <h3>서울특별시청</h3>',
                            '   <p>서울특별시 중구 태평로1가 31 | 서울특별시 중구 세종대로 110 서울특별시청<br />',
                            '       02-120 | 공공,사회기관 &gt; 특별,광역시청<br />',
                            '       <a href="http://www.seoul.go.kr" target="_blank">www.seoul.go.kr/</a>',
                            '   </p>',
                            '</div>'
                        ].join('');

                        var infowindow = new naver.maps.InfoWindow({
                            content: contentString,
                            maxWidth: 200,
                            backgroundColor: "#eee",
                            borderColor: "#2db400",
                            borderWidth: 5,
                            anchorSize: new naver.maps.Size(30, 30),
                            anchorSkew: true,
                            anchorColor: "#eee",
                            pixelOffset: new naver.maps.Point(20, -20)
                        });

                        naver.maps.Event.addListener(marker, "click", function(e) {
                            if (infowindow.getMap()) {
                                infowindow.close();
                            } else {
                                infowindow.open(map, marker);
                            }
                        });
                    }


