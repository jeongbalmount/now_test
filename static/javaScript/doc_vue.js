$(document).ready(function () {
        $('[data-toggle="popover"]').popover();
    });
    axios.defaults.xsrfCookieName = 'csrftoken';
    axios.defaults.xsrfHeaderName = 'x-CSRFToken';
    vars = input = document.querySelector('input');
    input.style.opacity = 0;

    var vm = new Vue({
        delimiters: ['[[', ']]'],
        el: '#app',
        data: {
            limitSize: 52428800,
            isHoverTrue: false,
            isSelectTrue: false,
            fileSize: 0,
            fileList: [],
            // 각 형식에 따른 값 딕셔너리
            URL_settings: {
                URL_fpsValue: 15,
                URL_scaleValue_select: "변환할 동영상 해상도(기본)",
                URL_start: "0",
                URL_end: "동영상 끝나는 시간",
            },
            URL_settings_2: {
                URL_fpsValue_2: 15,
                URL_scaleValue_select_2: "변환할 동영상 해상도(기본)",
                URL_start_2: "0",
                URL_end_2: "동영상 끝나는 시간",
            },
            firstFile_settings: {
                fpsValue_1: 15,
                scaleValue_select_1: "변환할 동영상 해상도(기본)",
                start_1: "0",
                end_1: "동영상 끝나는 시간",
            },
            secondFile_settings: {
                fpsValue_2: 15,
                scaleValue_select_2: "변환할 동영상 해상도(기본)",
                start_2: "0",
                end_2: "동영상 끝나는 시간",
            },
            // 설정 값을 보여주는 딕셔너리
            URL_showData: false,
            URL_showData_2: false,
            firstFile_showData: false,
            secondFile_showData: false,
            url_gif: '',
            url_gif_2: '',
            url_gif_name: '',
            url_gif_name_2: '',
            // 0값일때 원래 동영상 크기로 변환
            convertedFileUrl: [],
            fileNamesWithCheck: [],
            forConvertButton: [
                {
                    checkConverted: false, // 변환하기 버튼 누른 후
                    nowLoading: false, // 로딩중 버튼이 생성
                    loadingDone: false, // 로딩이 끝날때를 위한 값
                }
            ],
            fileSizeCheck: false,
            inputURL: '',
            inputURL_2: '',
            isURL_converted: false, // url이 서버로 넘어 갈때 화면 변화를 위한 값
            URL_button_clicked: true, // true여야 안보임
            fileTypes: [
                'video/avi',
                'video/x-flv',
                'video/x-ms-wmv',
                'video/quicktime',
                'video/mp4',
                'video/webm',
                'video/x-matroska',
                'video/mpeg'
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
        },
        // 설정값 캐싱
        mounted() {
            cached_data_URL = Object.assign({}, this.URL_settings);
            cached_data_URL_2 = Object.assign({}, this.URL_settings_2);
            cached_data_1 = Object.assign({}, this.firstFile_settings);
            cached_data_2 = Object.assign({}, this.secondFile_settings);
        },
        methods: {
            URL_appear: function(){
                if (this.URL_button_clicked == false){
                    this.URL_button_clicked = true;
                }else if(this.URL_button_clicked == true){
                    this.URL_button_clicked = false;
                }
            },
            // 6개 설정값 캐싱
            URL_save_change: function () {
                this.cached_data_URL = Object.assign({}, this.URL_settings);
                this.URL_showData = true;
            },
            URL_close_function: function () {
                this.URL_settings = Object.assign({}, this.cached_data_URL);
            },
            URL_save_change_2: function () {
                this.cached_data_URL_2 = Object.assign({}, this.URL_settings_2);
                this.URL_showData_2 = true;
            },
            URL_close_function_2: function () {
                this.URL_settings_2= Object.assign({}, this.cached_data_URL_2);
            },
            firstFile_save_change: function () {
                this.cached_data_1 = Object.assign({}, this.firstFile_settings);
                this.firstFile_showData = true;
            },
            firstFile_close_function: function () {
                this.firstFile_settings = Object.assign({}, this.cached_data_1);
            },
            secondFile_save_change: function () {
                this.cached_data_2 = Object.assign({}, this.secondFile_settings);
                this.secondFile_showData = true;
            },
            secondFile_close_function: function () {
                this.secondFile_settings = Object.assign({}, this.cached_data_2);
            },

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

            isNumber: function(input_value){
                return isNaN(input_value);
            },

            make_float: function(input_value){
                return Number(input_value).toFixed(2);
            },

            uploadFiles: function () {
                var vm = this;
                var verifiedURL;
                // url 형식 확인
                if (vm.inputURL !== '') {
                    verifiedURL = this.verifyURL(this.inputURL);
                    if (verifiedURL === false) {
                        alert("Url형식이 아닙니다");
                        return;
                    }
                    this.isHoverTrue = true;
                }
                if (vm.fileList.length === 0 && verifiedURL !== true) {
                    alert("파일이나 파일URL을 추가해 주세요")
                    return;
                }

                if (vm.fileList.length > 0) {
                    var form_files = new FormData();
                    if (vm.fileList.length === 1) {
                        if (vm.firstFile_settings.start_1 === ""){
                            alert("시작 시간을 적어주세요");
                            return;
                        }else if(vm.firstFile_settings.end_1 === ""){
                            alert("끝나는 시간을 적어주세요");
                            return;
                        }
                        if (vm.firstFile_settings.end_1 !== "동영상 끝나는 시간"){
                            if(vm.isNumber(vm.firstFile_settings.start_1) || vm.isNumber(vm.firstFile_settings.end_1)){
                                alert('0이상의 수를 적어주세요(소수점 2자리까지 설정됩니다).');
                                return;
                            }
                            if (vm.firstFile_settings.start_1 > vm.firstFile_settings.end_1){
                                alert('시작 시간이 끝나는 시간보다 큽니다. 수정해 주세요');
                                return;
                            }
                            if (vm.firstFile_settings.end_1 == 0 ){
                                alert('끝나는 시간을 수정해 주세요');
                                return;
                            }
                            if (vm.firstFile_settings.start_1 < 0 || vm.firstFile_settings.end_1 < 0){
                                alert('0이상의 수를 적어주세요(소수점 2자리까지 설정됩니다).');
                                return;
                            }
                        }else if(vm.firstFile_settings.end_1 == "동영상 끝나는 시간"){
                            if(vm.isNumber(vm.firstFile_settings.start_1)){
                                alert('0이상의 수를 적어주세요(소수점 2자리까지 설정됩니다).');
                                return;
                            }
                            if (vm.firstFile_settings.start_1 < 0){
                                alert('0이상의 수를 적어주세요(소수점 2자리까지 설정됩니다).');
                                return;
                            }
                            vm.firstFile_settings.end_1  = -1.0;
                        }

                        start_1_value = vm.make_float(vm.firstFile_settings.start_1);
                        end_1_value  = vm.make_float(vm.firstFile_settings.end_1);

                        form_files.append('first_uploaded_file', vm.fileList[0]);
                        form_files.append('scaleValue_select_1',vm.firstFile_settings.scaleValue_select_1);
                        form_files.append('fps_value_1', vm.firstFile_settings.fpsValue_1);
                        form_files.append('start_1', start_1_value);
                        form_files.append('end_1', end_1_value);


                    } else {
                        if (vm.firstFile_settings.start_1 === ""){
                            alert("시작 시간을 적어주세요");
                            return;
                        }else if(vm.firstFile_settings.end_1 === ""){
                            alert("끝나는 시간을 적어주세요");
                            return;
                        }else if(vm.secondFile_settings.start_2 === ""){
                            alert("시작 시간을 적어주세요");
                            return;
                        }else if(vm.secondFile_settings.end_2 === ""){
                            alert("끝나는 시간을 적어주세요");
                            return;
                        }
                        console.log(vm.firstFile_settings.end_1 == "동영상 끝나는 시간");
                        if (vm.firstFile_settings.end_1 !== "동영상 끝나는 시간" && vm.secondFile_settings.end_2 !== "동영상 끝나는 시간"){
                            if(vm.isNumber(vm.firstFile_settings.start_1) || vm.isNumber(vm.firstFile_settings.end_1) ||
                            vm.isNumber(vm.secondFile_settings.start_2) || vm.isNumber(vm.secondFile_settings.end_2)){
                                alert('0이상의 수를 적어주세요(소수점 2자리까지 설정됩니다).');
                                return;
                            }
                            if (vm.firstFile_settings.start_1 > vm.firstFile_settings.end_1 ||
                             vm.secondFile_settings.start_2 > vm.secondFile_settings.end_2){
                                alert('시작 시간이 끝나는 시간보다 큽니다. 수정해 주세요');
                                return;
                            }
                            if (vm.firstFile_settings.end_1 == 0 || vm.secondFile_settings.end_2 == 0){
                                alert('끝나는 시간을 수정해 주세요');
                                return;
                            }
                            if (vm.firstFile_settings.start_1 < 0 || vm.secondFile_settings.start_2 < 0
                                || vm.isNumber(vm.firstFile_settings.end_1) < 0 || vm.isNumber(vm.secondFile_settings.end_2) < 0){
                                alert('0이상의 수를 적어주세요(소수점 2자리까지 설정됩니다).');
                                return;
                            }
                        }else if(vm.firstFile_settings.end_1 == "동영상 끝나는 시간" && vm.secondFile_settings.end_2 !== "동영상 끝나는 시간"){
                            if(vm.isNumber(vm.firstFile_settings.start_1) || vm.isNumber(vm.secondFile_settings.start_2) || vm.isNumber(vm.secondFile_settings.end_2)){
                                alert('0이상의 수를 적어주세요(소수점 2자리까지 설정됩니다).');
                                return;
                            }
                            if (vm.firstFile_settings.start_1 < 0 || vm.secondFile_settings.start_2 < 0
                                || vm.isNumber(vm.secondFile_settings.end_2) < 0){
                                alert('0이상의 수를 적어주세요(소수점 2자리까지 설정됩니다).');
                                return;
                            }
                            if (vm.secondFile_settings.start_2 > vm.secondFile_settings.end_2){
                                alert('시작 시간이 끝나는 시간보다 큽니다. 수정해 주세요');
                                return;
                            }
                            if (vm.secondFile_settings.end_2 == 0 ){
                                alert('끝나는 시간을 수정해 주세요');
                                return;
                            }

                            vm.firstFile_settings.end_1 = -1.0;

                        }else if(vm.secondFile_settings.end_2 == "동영상 끝나는 시간" && vm.firstFile_settings.end_1 !== "동영상 끝나는 시간"){
                            if(vm.isNumber(vm.secondFile_settings.start_2) || vm.isNumber(vm.firstFile_settings.start_1) || vm.isNumber(vm.firstFile_settings.end_1)){
                                alert('0이상의 수를 적어주세요(소수점 2자리까지 설정됩니다).');
                                return;
                            }
                            if (vm.secondFile_settings.start_2 < 0 || vm.firstFile_settings.start_1 < 0
                                || vm.isNumber(vm.firstFile_settings.end_1) < 0){
                                alert('0이상의 수를 적어주세요(소수점 2자리까지 설정됩니다).');
                                return;
                            }
                            if (vm.firstFile_settings.start_1 > vm.firstFile_settings.end_1){
                                alert('시작 시간이 끝나는 시간보다 큽니다. 수정해 주세요');
                                return;
                            }
                            if (vm.firstFile_settings.end_1 == 0){
                                alert('끝나는 시간을 수정해 주세요');
                                return;
                            }

                            vm.secondFile_settings.end_2  = -1.0;

                        }else if(vm.firstFile_settings.end_1 == "동영상 끝나는 시간" && vm.secondFile_settings.end_2 == "동영상 끝나는 시간"){
                            if(vm.isNumber(vm.firstFile_settings.start_1) || vm.isNumber(vm.secondFile_settings.start_2)){
                                alert('0이상의 수를 적어주세요(소수점 2자리까지 설정됩니다).');
                                return;
                            }
                            if (vm.firstFile_settings.start_1 < 0 || vm.secondFile_settings.start_2 < 0){
                                alert('시작 시간을 수정해 주세요');
                                return;
                            }

                            vm.firstFile_settings.end_1 = -1.0;
                            vm.secondFile_settings.end_2 = -1.0;

                        }


                        start_1_value = vm.make_float(vm.firstFile_settings.start_1);
                        end_1_value  = vm.make_float(vm.firstFile_settings.end_1);
                        start_2_value = vm.make_float(vm.secondFile_settings.start_2);
                        end_2_value  = vm.make_float(vm.secondFile_settings.end_2);

                        form_files.append('first_uploaded_file', vm.fileList[0]);
                        form_files.append('second_uploaded_file', vm.fileList[1]);
                        form_files.append('scaleValue_select_1',vm.firstFile_settings.scaleValue_select_1);
                        form_files.append('scaleValue_select_2',vm.secondFile_settings.scaleValue_select_2);
                        form_files.append('fps_value_1', vm.firstFile_settings.fpsValue_1);
                        form_files.append('fps_value_2', vm.secondFile_settings.fpsValue_2);
                        form_files.append('start_1', start_1_value);
                        form_files.append('start_2', start_2_value);
                        form_files.append('end_1', end_1_value);
                        form_files.append('end_2', end_2_value);
                    }

                    vm.forConvertButton[0].checkConverted = true;
                    vm.forConvertButton[0].nowLoading = true;
                    this.isHoverTrue = true;

                    axios.post('/convert/upload/', form_files)
                        .then(function (res) {
                            if (vm.fileList.length === 1) {
                                vm.fileNamesWithCheck[0].convertedFileUrl = res.data.url_one;
                                vm.fileNamesWithCheck[0].fileUploaded = true;
                                vm.forConvertButton[0].nowLoading = false;
                                vm.forConvertButton[0].loadingDone = true;
                            } else {
                                vm.fileNamesWithCheck[0].convertedFileUrl = res.data.url_one;
                                vm.fileNamesWithCheck[0].fileUploaded = true;

                                vm.fileNamesWithCheck[1].convertedFileUrl = res.data.url_two;
                                vm.fileNamesWithCheck[1].fileUploaded = true;

                                vm.forConvertButton[0].nowLoading = false;
                                vm.forConvertButton[0].loadingDone = true;
                            }
                            vm.forConvertButton[0].checkConverted = true;
                            vm.fileSizeCheck = false;
                        })
                        .catch(function (err) {
                            err_data = err.response.data.err_message
                            error_message = err.response.data.err_message;
                            alert(error_message);
                            location.reload();
                            //vm.forConvertButton[0].nowLoading = false;
                        })
                } else {
                    if (vm.inputURL_2 === ""){
                        if (vm.URL_settings.URL_start === ""){
                            alert("시작 시간을 적어주세요");
                            return;
                        }else if(vm.URL_settings.URL_end === ""){
                            alert("끝나는 시간을 적어주세요");
                            return;
                        }
                    if (vm.URL_settings.URL_end !== "동영상 끝나는 시간"){
                            if(vm.isNumber(vm.URL_settings.URL_start) || vm.isNumber(vm.URL_settings.URL_end)){
                                alert('0이상의 수를 적어주세요(소수점 2자리까지 설정됩니다).');
                                return;
                            }
                            if (vm.URL_settings.URL_start > vm.URL_settings.URL_end){
                                alert('시작 시간이 끝나는 시간보다 큽니다. 수정해 주세요');
                                return;
                            }
                            if (vm.URL_settings.URL_end == 0){
                                alert('끝나는 시간을 수정해 주세요');
                                return;
                            }
                            if (vm.URL_settings.URL_start < 0 || vm.URL_settings.URL_end < 0){
                                alert('0이상의 수를 적어주세요(소수점 2자리까지 설정됩니다).');
                                return;
                            }
                        }else if(vm.URL_settings.URL_end == "동영상 끝나는 시간"){
                            if(vm.isNumber(vm.URL_settings.URL_start)){
                                alert('0이상의 수를 적어주세요(소수점 2자리까지 설정됩니다).');
                                return;
                            }
                            if (vm.URL_settings.URL_start < 0){
                                alert('시작 시간을 수정해 주세요');
                                return;
                            }
                            vm.URL_settings.URL_end  = -1.0;
                        }

                        URL_start_value = vm.make_float(vm.URL_settings.URL_start);
                        URL_end_value  = vm.make_float(vm.URL_settings.URL_end);

                        var sendURL = {'uploadURL': vm.inputURL,'URL_fps_value': vm.URL_settings.URL_fpsValue,
                        'URL_scaleValue_select': vm.URL_settings.URL_scaleValue_select, 'URL_start': URL_start_value, 'URL_end': URL_end_value};
                    } else {
                        if (vm.URL_settings.URL_end !== "동영상 끝나는 시간" && vm.URL_settings_2.URL_end_2 !== "동영상 끝나는 시간"){
                            if(vm.isNumber(vm.URL_settings.URL_start) || vm.isNumber(vm.URL_settings.URL_end) ||
                            vm.isNumber(vm.URL_settings_2.URL_start_2) || vm.isNumber(vm.URL_settings_2.URL_end_2)){
                                alert('0이상의 수를 적어주세요(소수점 2자리까지 설정됩니다).');
                                return;
                            }
                            if (vm.URL_settings.URL_end > vm.URL_settings.URL_end ||
                             vm.URL_settings_2.URL_start_2 > vm.URL_settings_2.URL_end_2){
                                alert('시작 시간이 끝나는 시간보다 큽니다. 수정해 주세요');
                                return;
                            }
                            if (vm.URL_settings.URL_end == 0 || vm.URL_settings_2.URL_end_2 == 0){
                                alert('끝나는 시간을 수정해 주세요');
                                return;
                            }
                            if (vm.URL_settings.URL_start < 0 || vm.URL_settings_2.URL_start_2 < 0
                                || vm.isNumber(vm.URL_settings.URL_end) < 0 || vm.isNumber(vm.URL_settings_2.URL_end_2) < 0){
                                alert('0이상의 수를 적어주세요(소수점 2자리까지 설정됩니다).');
                                return;
                            }
                        }else if(vm.URL_settings.URL_end == "동영상 끝나는 시간" && vm.URL_settings_2.URL_end_2 !== "동영상 끝나는 시간"){
                            if(vm.isNumber(vm.URL_settings.URL_start) || vm.isNumber(vm.URL_settings_2.URL_start_2) || vm.isNumber(vm.URL_settings_2.URL_end_2)){
                                alert('0이상의 수를 적어주세요(소수점 2자리까지 설정됩니다).');
                                return;
                            }
                            if (vm.URL_settings.URL_start < 0 || vm.URL_settings_2.URL_start_2 < 0
                                || vm.isNumber(vm.URL_settings_2.URL_endt_2) < 0){
                                alert('0이상의 수를 적어주세요(소수점 2자리까지 설정됩니다).');
                                return;
                            }
                            if (vm.URL_settings_2.URL_start_2 > vm.URL_settings_2.URL_end_2){
                                alert('시작 시간이 끝나는 시간보다 큽니다. 수정해 주세요');
                                return;
                            }
                            if (vm.URL_settings_2.URL_end_2 == 0 ){
                                alert('끝나는 시간을 수정해 주세요');
                                return;
                            }

                            vm.URL_settings.URL_end = -1.0;

                        }else if(vm.URL_settings_2.URL_end_2 == "동영상 끝나는 시간" && vm.URL_settings.URL_end !== "동영상 끝나는 시간"){
                            if(vm.isNumber(vm.URL_settings_2.URL_start_2) || vm.isNumber(vm.URL_settings.URL_start) || vm.isNumber(vm.URL_settings.URL_end)){
                                alert('0이상의 수를 적어주세요(소수점 2자리까지 설정됩니다).');
                                return;
                            }
                            if (vm.URL_settings_2.URL_start_2 < 0 || vm.URL_settings.URL_start < 0
                                || vm.isNumber(vm.URL_settings.URL_end) < 0){
                                alert('0이상의 수를 적어주세요(소수점 2자리까지 설정됩니다).');
                                return;
                            }
                            if (vm.URL_settings.URL_start > vm.URL_settings.URL_end){
                                alert('시작 시간이 끝나는 시간보다 큽니다. 수정해 주세요');
                                return;
                            }
                            if (vm.URL_settings.URL_end == 0){
                                alert('끝나는 시간을 수정해 주세요');
                                return;
                            }

                            vm.URL_settings_2.URL_end_2  = -1.0;

                        }else if(vm.URL_settings.URL_end == "동영상 끝나는 시간" && vm.URL_settings_2.URL_end_2 == "동영상 끝나는 시간"){
                            if(vm.isNumber(vm.URL_settings.URL_start) || vm.isNumber(vm.URL_settings_2.URL_start_2)){
                                console.log(vm.URL_settings.URL_start)
                                console.log(vm.URL_settings_2.URL_start_2)
                                alert('0이상의 수를 적어주세요(소수점 2자리까지 설정됩니다).');
                                return;
                            }
                            if (vm.URL_settings.URL_start < 0 || vm.URL_settings_2.URL_start_2 < 0){
                                alert('시작 시간을 수정해 주세요');
                                return;
                            }

                            vm.URL_settings.URL_end = -1.0;
                            vm.URL_settings_2.URL_end_2 = -1.0;

                        }
                        URL_start_value = vm.make_float(vm.URL_settings.URL_start);
                        URL_start_value_2 = vm.make_float(vm.URL_settings_2.URL_start_2);
                        URL_end_value  = vm.make_float(vm.URL_settings.URL_end);
                        URL_end_value_2  = vm.make_float(vm.URL_settings_2.URL_end_2);

                        var sendURL = {'uploadURL': vm.inputURL, 'uploadURL_2': vm.inputURL_2,
                        'URL_fps_value': vm.URL_settings.URL_fpsValue,'URL_fps_value_2': vm.URL_settings_2.URL_fpsValue_2,
                         'URL_scaleValue_select': vm.URL_settings.URL_scaleValue_select, 'URL_scaleValue_select_2': vm.URL_settings_2.URL_scaleValue_select_2,
                         'URL_start': URL_start_value, 'URL_start_2': URL_start_value_2,
                         'URL_end': URL_end_value, 'URL_end_2': URL_end_value_2};
                    }
                    vm.forConvertButton[0].checkConverted = true;
                    vm.forConvertButton[0].nowLoading = true;

                    axios.post('/convert/urlupload/', sendURL)
                        .then(function (res) {
                            if (vm.inputURL_2 == "") {
                                vm.fileNamesWithCheck.push({
                                fileName: res.data.file_name,
                                convertedFileUrl: res.data.url_one,
                                fileUploaded : true,
                                checkConverted : true,
                                nowLoading : false,
                                loadingDone : true
                            });
                            } else {
                                vm.url_gif = res.data.url_one;
                                vm.url_gif_2 = res.data.url_two;
                                vm.url_gif_name = res.data.file_name;
                                vm.url_gif_name_2 = res.data.file_name_2;
                            }
                            // vm.fileNamesWithCheck.push({
                            //     fileName: res.data.file_name,
                            //     convertedFileUrl: res.data.uploaded_file_url,
                            //     // vm.fileNamesWithCheck[0].convertedFileUrl = res.data.url_one;
                            //     // vm.fileNamesWithCheck[0].fileUploaded = true;

                            //     // vm.fileNamesWithCheck[1].convertedFileUrl = res.data.url_two;
                            //     // vm.fileNamesWithCheck[1].fileUploaded = true;
                            //     fileUploaded: true,
                            // });
                            // vm.isURL_converted = true; // url이 넘어 갔는지
                            vm.forConvertButton[0].checkConverted = true;
                            // vm.forConvertButton[0].nowLoading = false;
                            // vm.forConvertButton[0].loadingDone = true;
                            vm.fileSizeCheck = false
                            vm.isHoverTrue = true;
                        })
                        .catch(function (err) {
                            console.log(err);
                            // console.log(err.response);
                            // console.log(err.response.data);
                            err_data = err.data.response.err_message
                            // error_message = err.data.err_message;
                            alert(error_message);
                            location.reload();
                            //vm.forConvertButton[0].nowLoading = false;
                        })
                }
            },

            add_files: function (event) {
                if (this.forConvertButton[0].checkConverted == true) {
                    alert('새로고침 후에 사용해 주세요');
                    return;
                } else if (this.fileList.length == 2) {
                    alert('파일 최대 2개까지 선택가능');
                    return;
                }

                files = event.target.files;
                this.addFileSize(files);

                for (file of files) {
                    // 파일 타입 확인
                    if (!this.validFileType(file.type)) {
                        alert("변환할 수 있는 파일이 아닙니다");
                        this.minusFileSize(files);
                        return;
                    }
                }
                var fileCountLimit = this.fileList.length + files.length;

                if (fileCountLimit > 2) {
                    alert("파일 최대 2개까지 선택가능");
                    this.minusFileSize(files);
                    return;
                } else if (this.fileSize > this.limitSize) {
                    alert("파일 총 크기 제한 50MB");
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
                this.fileSizeCheck = true;
                this.isSelectTrue = true;
                this.URL_button_clicked = true; // true여야 안보임
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
                this.fileSize -= this.fileList[index].size;
                this.fileList.splice(index, 1);
                this.fileNamesWithCheck.splice(index, 1);
                if (this.fileList.length == 0) {
                    this.isSelectTrue = false;
                    this.fileSizeCheck = false;
                }
            },
            onDrop: function (event) {
                if (this.forConvertButton[0].checkConverted == true) {
                    alert('새로고침 후에 사용해 주세요');
                    this.isHoverTrue = true;
                    return;
                } else if (this.fileList.length == 2) {
                    alert('파일 최대 2개까지 선택가능');
                    this.isHoverTrue = false;
                    return;
                }
                this.className += ' hovered';
                var files = event.dataTransfer.files;

                this.addFileSize(files);

                for (file of files) {
                    if (!this.validFileType(file.type)) {
                        alert("변환할 수 있는 파일이 아닙니다");
                        this.minusFileSize(files);
                        this.isHoverTrue = false;
                        return;
                    } else if (this.fileNamesWithCheck.length != 0) {
                        if (this.fileNamesWithCheck[0].fileName == file.name) {
                            alert("같은 이름의 파일을 넣을 수 없습니다.");
                            this.minusFileSize(files);
                            this.isHoverTrue = false;
                            return;
                        }
                    }
                }
                var fileCountLimit = this.fileList.length + files.length;

                if (fileCountLimit > 2) {
                    alert("파일 최대 2개까지 선택가능");
                    this.minusFileSize(files);
                    return;
                } else if (this.fileSize > this.limitSize) {
                    alert("파일 총 크기 제한 50MB");
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
                this.fileSizeCheck = true;
                this.isSelectTrue = true;
                this.isHoverTrue = false;
                this.URL_button_clicked = true;
            },

            onDragOver: function (event) {
                // event.stopPropagation();
                // event.preventDefault();

                this.isHoverTrue = true;
            },

            onDragLeave: function (event) {
                // event.stopPropagation();
                // event.preventDefault();

                this.isHoverTrue = false;
            },

            validFileType: function (fileType) {
                return this.fileTypes.includes(fileType);
            },

            addFileSize: function (files) {
                for (file of files) {
                    this.fileSize += file.size;
                }
            },

            minusFileSize: function (files) {

                for (file of files) {
                    this.fileSize = this.fileSize - file.size;
                }

            }
        },
    });