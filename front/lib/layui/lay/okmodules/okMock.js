"use strict";
let version = 'v1.0.0'
let service = 'http://127.0.0.1:8000'
layui.define([], function (exprots) {
    let okMock = {
        api: {
            login: service + "/api/" + version + "/login",
            public: service + "/api/" + version + "/public",
            logout: service + "/api/" + version + "/logout",
            change: service + "/api/" + version + "/change",
            navs: service + "/api/" + version + "/navs",
            notice: service + "/api/" + version + "/notice",
            dashboard: service + "/api/" + version + "/dashboard/dashboard",
            listUser: service + "/api/" + version + "/user/users",
            submitProcess: service + "/api/" + version + "/process/submitProcess",
            handleProcess: service + "/api/" + version + "/process/handleProcess",
            reviewProcess: service + "/api/" + version + "/process/reviewProcess",
            attendance: service + "/api/" + version + "/attendance/attendance",
            atLeader: service + "/api/" + version + "/process/atLeader",
            abnormalAttendance: service + "/api/" + version + "/attendance/abnormalAttendance",
            holidayHandle: service + "/api/" + version + "/attendance/holidayHandle",
            personalSetting: service + "/api/" + version + "/setting/personalSetting",
            securitySetting: service + "/api/" + version + "/setting/securitySetting",
            systemSetting: service + "/api/" + version + "/setting/systemSetting",
            report: service + "/api/" + version + "/report/report",
            batch: service + "/api/" + version + "/user/batch",
            department: service + "/api/" + version + "/user/department",
        }
    };
    exprots("okMock", okMock);
});
