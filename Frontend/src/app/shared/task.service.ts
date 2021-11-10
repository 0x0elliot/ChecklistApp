import { Injectable } from "@angular/core";
import { HttpClient, HttpHeaders } from "@angular/common/http";
import { AuthService } from "./authentication.service";

@Injectable()
export class TaskService{
    readonly rootUrl = "http://localhost:4200/api/v1";
    constructor(private http: HttpClient, private auth : AuthService) {}

    addTask(task_name) {
        const body = {
            'task_name' : task_name
        }

        return this.http.post(this.rootUrl + '/taskcreate/', body);
    }

    fetchTasks() {

        const body = {}

        return this.http.get(this.rootUrl + '/tasklist/', body);
    }

    deleteTask(task_id) {
        const body = {
            'task_id' : task_id,
        }

        return this.http.post(this.rootUrl + '/taskdelete/', body);
    }
}