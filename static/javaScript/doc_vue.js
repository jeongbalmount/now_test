$(document).ready(function () {
    $('[data-toggle="popover"]').popover();
});
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'x-CSRFToken';
var input = document.querySelector('input');
input.style.opacity = 0;

var vm = new Vue({
    delimiters: ['[[', ']]'],
    el: '#app',
    data: {
        limitSize: 52428800, // 파일 최대 크기 50MB 넘지 않도록
        isHoverTrue: false, // 파일이 박스에 드래그된 상태인지 아닌지 확인
        isSelectTrue: false, // url이 아닌 파일이 들어가면 url없애기 위한 변수
        fileSize: 0, // 파일 사이즈
        fileList: [], // 실제 파일을 담는 리스트
        fpsValue_1: 15,
        fpsValue_2: 15,
        convertedFileUrl: [],
        fileNamesWithCheck: [
        ], // 파일 이름을 저장하고 파일 이름이 저장 됨과 동시에 백으로 넘어 갔다는걸 체크하는 부분도 저장
        forConvertButton: [
            {
                checkConverted: false,
                nowLoading: false,
                loadingDone: false,
            }
        ],
        fileSizeCheck: false, // 파일 전체 크기
        inputURL: '', // 전달할 url이 들어 있다.
        isURL: false,
        fileTypes: [
            'video/avi',
            'video/x-flv',
            'video/x-ms-wmv',
            'video/quicktime', //
            'video/mp4',
            'video/webm',
            'video/x-matroska',
             'video/mpeg'//
        ],
        fileEndTypes: [
            'avi',
            'flv',
            'wmv',
            'mov',
            'mp4',
            'webm',
            'mkv',
            'mpeg',
        ],
        uploadPercentage: 0,
    },
    methods: {
        // 기본적인 url인지 확인
        verifyURL: function (checkURL) {
            console.log("verifyURL");
            var url = checkURL;
            var pattern = /(ftp|http|https):\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-\/]))?/;
            var fileExtend = this.verifyExtends(url);
            console.log(fileExtend);
            if (pattern.test(url) && fileExtend) {
                return true;
            } else {
                return false;
            }
        },
        // video형식 파일인지 확인
        verifyExtends: function (url) {
            var fileExtends = url.split(/\#|\?/)[0].split('.').pop().trim();
            console.log(fileExtends)
            var lowerCase = fileExtends.toLowerCase()
            if (this.fileEndTypes.includes(fileExtends)) {
                return true;
            }
            else {
                return false;
            }
        },

        uploadFiles: function () {
            var vm = this;
            var verifiedURL;

            if (vm.inputURL !== '') {
                verifiedURL = this.verifyURL(this.inputURL);
                if (verifiedURL === false) {
                    alert("Url형식이 아닙니다");
                    return;
                }
                this.isHoverTrue = true;
            }
            // 파일이나 url이 아무것도 없을때
            if (vm.fileList.length === 0 && verifiedURL !== true) {
                alert("파일을 추가해 주세요")
                return;
            }

            vm.forConvertButton[0].checkConverted = true;
            vm.forConvertButton[0].nowLoading = true;
            var form = new FormData();
            // 파일 리스트에 아무것도 없으면 url이 들어온것으로 간주
            if (vm.fileList.length > 0) {
                if (vm.fileList.length === 1) {
                    vm.fpsValue_2 = 0;
                    form.append('first_uploaded_file', vm.fileList[0]);
                    form.append('fps_value_1', vm.fpsValue_1);
                    form.append('fps_value_2', vm.fpsValue_2);
                } else {
                    form.append('first_uploaded_file', vm.fileList[0]);
                    form.append('second_uploaded_file', vm.fileList[1]);
                    form.append('fps_value_1', vm.fpsValue_1);
                    form.append('fps_value_2', vm.fpsValue_2);
                }
                axios.post('/convert/upload/', form)
                    .then(function (res) {
                        console.log("POST RES", res);
                        if (vm.fileList.length === 1) {
                            vm.fileNamesWithCheck[0].convertedFileUrl = res.data.url_one;
                            vm.fileNamesWithCheck[0].fileUploaded = true;
                            vm.forConvertButton[0].nowLoading = false;
                            vm.forConvertButton[0].loadingDone = true;
                            console.log(vm.uploadPercentage)
                        } else {
                            vm.fileNamesWithCheck[0].convertedFileUrl = res.data.url_one;
                            vm.fileNamesWithCheck[0].fileUploaded = true;

                            vm.fileNamesWithCheck[1].convertedFileUrl = res.data.url_two;
                            vm.fileNamesWithCheck[1].fileUploaded = true;

                            vm.forConvertButton[0].nowLoading = false;
                            vm.forConvertButton[0].loadingDone = true;
                        }
                        // 변환하기 버튼이 뜨도록 만드는 checkconverted버튼 true
                        vm.forConvertButton[0].checkConverted = true;
                        // 보내고 나서 파일 크기 나타내는 부분 없애기
                        vm.fileSizeCheck = false;
                    })
                    .catch(function (err) {
                        alert("새로고침 후 다시 사용해 주세요");
                        vm.forConvertButton[0].nowLoading = false;
                        console.log("GET ERR", err);
                    })
            } else {
                // url 보냈을때 부분
                // url은 폼데이터가 아닌 딕셔너리 형식으로 보냄
                var sendURL = { uploadURL: vm.inputURL };
                vm.isURL = true;
                // 나중에 파일 변환을 url기반 파일이냐 일반파일이냐 구분 하기 위해
                // 만든 변수
                console.log(vm.inputURL);

                axios.post('/convert/urlupload/', sendURL)
                    .then(function (res) {
                        console.log("POST RES", res);
                        // push하는 이유는 vue v-if를 조정시키기 위해서이다.
                        vm.fileNamesWithCheck.push({
                            fileName: res.data.file_name,
                            convertedFileUrl: res.data.uploaded_file_url,
                            fileUploaded: true,
                        });
                        // 업로드 버튼 없애기
                        vm.forConvertButton[0].checkConverted = true;
                        // 로딩 스핀 나오게 하기
                        vm.forConvertButton[0].nowLoading = false;
                        // 모든게 완료 되었다는 것 보여주기
                        vm.forConvertButton[0].loadingDone = true;
                        // 파일 크기 없앰
                        vm.fileSizeCheck = false
                    })
                    .catch(function (err) {
                        alert("새로고침 후 다시 사용해 주세요");
                        vm.forConvertButton[0].nowLoading = false;
                        console.log("GET ERR", err);
                    })
            }
        },

        add_files: function (event) {
            if (this.forConvertButton[0].checkConverted == true) {
                // 이미 업로드된 파일이 있으면 더이상 파일 못 받게 하기
                alert('새로고침 후에 사용해 주세요');
                return;
            } else if (this.fileList.length == 2) {
                alert('파일 최대 2개까지 선택가능');
                return;
            }
            // 파일 직접 찾아서 넣는 부분
            console.log(event.target.files + " 방금 파일 더해짐");
            files = event.target.files;
            // 파일 크기 업데이트
            this.addFileSize(files);

            for (file of files) {
                console.log(typeof (file.type));
                console.log(file.type);
                if (!this.validFileType(file.type)) {
                    // 비디오 파일이 아니면 alert하고 더했던 파일 크기 줄이기
                    alert("변환할 수 있는 파일이 아닙니다");
                    this.minusFileSize(files);
                    return;
                }
            }
            // 파일 개수 업데이트
            var fileCountLimit = this.fileList.length + files.length;
            console.log(fileCountLimit + " 파일 개수");

            if (fileCountLimit > 2) {
                //파일 개수 체크
                alert("파일 최대 2개까지 선택가능");
                this.minusFileSize(files);
                return;
            } else if (this.fileSize > this.limitSize) {
                alert("파일 총 크기 제한 50MB");
                console.log(this.fileSize);
                console.log(typeof (files));
                this.minusFileSize(files);
                return;
            }

            for (file of files) {
                this.fileList.push(file);
                this.fileNamesWithCheck.push({
                    fileName: file.name,
                    fileUploaded: false,
                });
            }
            // 파일 사이즈를 보여주도록 true를 준다.
            this.fileSizeCheck = true;
            // url이 아닌 파일이 선택되어서 url을 지우게 만든다.
            this.isSelectTrue = true;
        },

        returnedFileSize: function (number) {
            if (number < 1024) {
                return number + 'bytes';
            } else if (number >= 1024 && number < 1048576) {
                return (number / 1024).toFixed(1) + 'KB';
            } else if (number >= 1048576) {
                return (number / 1048576).toFixed(1) + 'MB';
            }
        },
        remove_todo: function (index) {
            console.log(index);
            console.log(this.fileList[index].size);
            // 총사이즈에서 지우는 파일 크기 빼는 부분
            this.fileSize -= this.fileList[index].size;
            // 파일 리스트에서 그 파일 지우기
            this.fileList.splice(index, 1);
            console.log(this.fileList.length + " 파일 리스트 길이");
            // 파일 이름 지우기
            this.fileNamesWithCheck.splice(index, 1);
            if (this.fileList.length == 0) {
                // 모든 파일 지운 상태면 url 살리고 파일 크기 보여주는 부분 없앤다.
                this.isSelectTrue = false;
                this.fileSizeCheck = false;
            }
        },
        onDrop: function (event) {
            // drag&drop으로 파일 받는 부분
            if (this.forConvertButton[0].checkConverted == true) {
                alert('새로고침 후에 사용해 주세요');
                // 이미 업로드된 파일이 있으면 더이상 파일 못 받게 하기
                this.isHoverTrue = false;
                return;
            } else if (this.fileList.length == 2) {
                alert('파일 최대 2개까지 선택가능');
                this.isHoverTrue = false;
                return;
            }

            console.log("ondrop");
            // event.stopPropagation();
            // event.preventDefault();

            console.log('dragEnter');
            // 파일이 박스안에 드래그 되면 .hovered 스타일 추가
            this.className += ' hovered';
            // 드래그로 들어온 파일들
            var files = event.dataTransfer.files;


            this.addFileSize(files);
            console.log(this.fileSize);

            for (file of files) {
                console.log(typeof (file.type));
                console.log(file.type);
                if (!this.validFileType(file.type)) {
                    alert("변환할 수 있는 파일이 아닙니다");
                    this.minusFileSize(files);
                    // 변환할 수 없다는거 보여주고 원래 상태로 돌아오기
                    this.isHoverTrue = false;
                    return;
                } else if (this.fileNamesWithCheck.length != 0) {
                    if (this.fileNamesWithCheck[0].fileName == file.name) {
                        alert("같은 이름의 파일을 넣을 수 없습니다.");
                        this.minusFileSize(files);
                        // 변환할 수 없다는거 보여주고 원래 상태로 돌아오기
                        this.isHoverTrue = false;
                        return;
                    }
                }
            }
            console.log(this.fileList.length, files.length)
            var fileCountLimit = this.fileList.length + files.length;

            if (fileCountLimit > 2) {
                //파일 개수 체크
                alert("파일 최대 2개까지 선택가능");
                this.minusFileSize(files);
                return;
            } else if (this.fileSize > this.limitSize) {
                alert("파일 총 크기 제한 50MB");
                console.log(this.fileSize);
                console.log(typeof (files));
                this.minusFileSize(files);
                return;
            }


            for (file of files) {
                this.fileList.push(file);
                this.fileNamesWithCheck.push({
                    fileName: file.name,
                    fileUploaded: false,
                });
            }
            this.fileSizeCheck = true; //파일 사이즈 나오게함
            this.isSelectTrue = true;// url없애기
            this.isHoverTrue = false;// 파일 제대로 놓으면 원래대로 놓기
        },

        onDragOver: function (event) {
            // event.stopPropagation();
            // event.preventDefault();

            console.log('dragOver');
            this.isHoverTrue = true;
        },

        onDragLeave: function (event) {
            // event.stopPropagation();
            // event.preventDefault();

            console.log('dragLeave');
            this.isHoverTrue = false;
        },

        validFileType: function (fileType) {
            console.log(this.fileTypes.includes(fileType));
            return this.fileTypes.includes(fileType);
        },

        addFileSize: function (files) {
            for (file of files) {
                this.fileSize += file.size;
                console.log(this.fileSize);
            }
        },

        minusFileSize: function (files) {
            console.log(file.size);
            console.log(this.fileSize);

            for (file of files) {
                this.fileSize = this.fileSize - file.size;
            }

            console.log(this.fileSize);
        }
    },
});