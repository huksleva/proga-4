const { createApp } = Vue;

createApp({
    data() {
        return {
            file1: null,           // File object для отправки
            file1NameValue: 'Файл не выбран',  // Строка для отображения
            file2: null,
            file2NameValue: 'Файл не выбран',  // Строка для отображения
            sizeResult: null,
            pictureResult: null,
            lastUpload: null,
            loading: false
        }
    },


    async mounted() {
        await this.loadLastUpload();
    },

    methods: {
        selectFile1(event) {
            if (event.target.files.length > 0) {
                this.file1NameValue = event.target.files[0].name;
                this.file1 = event.target.files[0];
            }
        },

        selectFile2(event) {
            if (event.target.files.length > 0) {
                const file = event.target.files[0];

                this.file2NameValue = file.name;
                this.file2 = file;
            }
        },

        async uploadSize() {
            if (!this.file1) return;

            const formData = new FormData();
            formData.append('image', this.file1);

            const response = await fetch('/size2json', {method: 'POST', body: formData});
            const data = await response.json();

            if (response.ok) {
                // Создаём Blob с JSON и открываем в новой вкладке
                const blob = new Blob([JSON.stringify(data, null, 2)], {type: 'application/json'});
                const url = URL.createObjectURL(blob);
                window.open(url, '_blank');
            } else {
                alert(data.result);
            }
        },

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
                    localStorage.setItem('lastUpload', JSON.stringify(data));
                } else {
                    alert(`Ошибка: ${data.result}`);
                }
            } catch (error) {
                alert(`Ошибка: ${error.message}`);
            }

            this.loading = false;
        },

        async loadLastUpload() {
            const local = localStorage.getItem('lastUpload');
            if (local) {
                this.lastUpload = JSON.parse(local);
                return;
            }

            try {
                const response = await fetch('/lastUpload');
                if (response.ok) {
                    this.lastUpload = await response.json();
                }
            } catch (error) {
                console.log('Нет сохранённых файлов');
            }
        },

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