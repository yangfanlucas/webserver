<<<<<<< HEAD
﻿function showNotification() {
                if(window.Notification) {
                    if(window.Notification.permission == "granted") {
                        var notification = new Notification('消息提醒测试中', {
                            body: "测试test"
                        });
                        notification.onclick = function () {
            		window.open("/hpnt/chat");
            		notification.close();
	       };
                   } else {
                        window.Notification.requestPermission();
                    };
                } else alert('你的浏览器不支持此消息提示功能，请使用chrome内核的浏览器！');
=======
﻿function showNotification() {
                if(window.Notification) {
                    if(window.Notification.permission == "granted") {
                        var notification = new Notification('消息提醒测试中', {
                            body: "测试test"
                        });
                        notification.onclick = function () {
            		window.open("/hpnt/chat");
            		notification.close();
	       };
                   } else {
                        window.Notification.requestPermission();
                    };
                } else alert('你的浏览器不支持此消息提示功能，请使用chrome内核的浏览器！');
>>>>>>> 68743d3 (2024.5.2(ssh))
            };