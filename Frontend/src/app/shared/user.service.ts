import { Injectable } from "@angular/core";
import { HttpClient, HttpHeaders } from '@angular/common/http'
import { User } from "./user.model";

@Injectable()
export class UserService {
    readonly rootUrl = "http://localhost:8000";
    constructor(private http: HttpClient) { }

    registerUser(Name, Email, Password) {
        const body = {
            name : Name,
            password : Password,
            email : Email,
        }

        return this.http.post(this.rootUrl + '/api/v1/register', body);
    }

    LoginUser(Email, Password) {
        const body = {
            email : Email,
            password : Password,
        }
        
        return this.http.post(this.rootUrl + '/api/v1/login', body);
    }

}