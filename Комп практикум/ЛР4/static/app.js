const { createApp } = Vue;

createApp({
    data() {
        return {
            file1: null,
            file2: null,
            sizeResult: null,
            pictureResult: null,
            lastUpload: null,
            loading: false
        }
    },

    // Загружается при открытии страницы
    async mounted() {
        await this.loadLastUpload();
    },

    methods: {
        // Выбор файла для формы 1
        selectFile1(event) {
            this.file1 = event.target.files[0];
        },

        // Выбор файла для формы 2
        selectFile2(event) {
            this.file2 = event.target.files[0];
        },

        // Отправка на /size2json
        async uploadSize() {
            if (!this.file1) return;

            this.loading = true;
            this.sizeResult = null;

            try {
                const formData = new FormData();
                formData.append('image', this.file1);

                const response = await fetch('/size2json', {
                    method: 'POST',
                    body: formData
                });

                const data = await response.json();

                if (response.ok) {
                    this.sizeResult = {
                        error: false,
                        message: `Ширина: ${data.width}, Высота: ${data.height}`
                    };
                } else {
                    this.sizeResult = {
                        error: true,
                        message: ${data.result}`
                    };
                }
            } catch (error) {
                this.sizeResult = {
                    error: true,
                    message: `Ошибка: ${error.message}`
                };
            }

            this.loading = false;
        },

        // Отправка на /showPicture
        async uploadPicture() {
            if (!this.file2) return;

            this.loading = true;
            this.pictureResult = null;

            try {
                const formData = new FormData();
                formData.append('image', this.file2);

                const response = await fetch('/showPicture', {
                    method: 'POST',
                    body: formData
                });

                const data = await response.json();

                if (response.ok) {
                    this.pictureResult = data;

                    // Сохраняем в localStorage
                    localStorage.setItem('lastUpload', JSON.stringify(data));
                } else {
                    alert(`Ошибка: ${data.result}`);
                }
            } catch (error) {
                alert(`Ошибка: ${error.message}`);
            }

            this.loading = false;
        },

        // Загрузка последнего файла
        async loadLastUpload() {
            // Сначала пробуем из localStorage
            const local = localStorage.getItem('lastUpload');
            if (local) {
                this.lastUpload = JSON.parse(local);
                return;
            }

            // Если нет, запрашиваем у сервера
            try {
                const response = await fetch('/lastUpload');
                if (response.ok) {
                    this.lastUpload = await response.json();
                }
            } catch (error) {
                console.log('Нет сохранённых файлов');
            }
        },

        // Очистка файлов
        async clearUploads() {
            if (!confirm('Удалить все загруженные файлы?')) return;

            try {
                const response = await fetch('/clearUploads', { method: 'POST' });
                if (response.ok) {
                    this.pictureResult = null;
                    this.lastUpload = null;
                    localStorage.removeItem('lastUpload');
                    alert('Файлы очищены');
                }
            } catch (error) {
                alert(`Ошибка: ${error.message}`);
            }
        }
    }
}).mount('#app');