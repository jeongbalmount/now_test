$(document).ready(function () {
    $('[data-toggle="popover"]').popover();
});
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'x-CSRFToken';
vars =  input = document.querySelector('input');
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
        fpsValue_1: 15,
        fpsValue_2: 15,
        scaleValue_select:0,
        width_value:0,
        height_value:0,
        convertedFileUrl: [],
        fileNamesWithCheck: [
        ],
        forConvertButton: [
            {
                checkConverted: false,
                nowLoading: false,
                loadingDone: false,
            }
        ],
        fileSizeCheck: false,
        inputURL: '',
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
            if (vm.fileList.length === 0 && verifiedURL !== true) {
                alert("파일을 추가해 주세요")
                return;
            }

            vm.forConvertButton[0].checkConverted = true;
            vm.forConvertButton[0].nowLoading = true;
            var form = new FormData();

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
                axios.post('/convert/upload/', form, {xsrfCookieName: 'csrftoken', xsrfHeaderName: 'X-CSRFToken'})
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
                        alert("새로고침 후 다시 사용해 주세요");
                        vm.forConvertButton[0].nowLoading = false;

                    })
            } else {
                var sendURL = { uploadURL: vm.inputURL };
                vm.isURL = true;
                axios.post('/convert/urlupload/', sendURL, {xsrfCookieName: 'csrftoken', xsrfHeaderName: 'X-CSRFToken'})
                    .then(function (res) {

                        vm.fileNamesWithCheck.push({
                            fileName: res.data.file_name,
                            convertedFileUrl: res.data.uploaded_file_url,
                            fileUploaded: true,
                        });
                        vm.forConvertButton[0].checkConverted = true;
                        vm.forConvertButton[0].nowLoading = false;
                        vm.forConvertButton[0].loadingDone = true;
                        vm.fileSizeCheck = false
                    })
                    .catch(function (err) {
                        alert("새로고침 후 다시 사용해 주세요");
                        vm.forConvertButton[0].nowLoading = false;

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
                this.isHoverTrue = false;
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