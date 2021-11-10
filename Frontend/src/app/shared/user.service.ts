import { Injectable } from "@angular/core";
import { HttpClient} from '@angular/common/http'
import { User } from "./user.model";

@Injectable()
export class UserService {
    readonly rootUrl = "http://localhost:4200";
    constructor(private http: HttpClient) { }

    registerUser(Name, Email, Password) {
        const body = {
            name : Name,
            password : Password,
            email : Email,
        }

        return this.http.post(this.rootUrl + '/api/v1/register/', body);
    }

    LoginUser(Email, Password) {
        const body = {
            email : Email,
            password : Password,
        }
        
        return this.http.post(this.rootUrl + '/api/v1/login/', body);
    }

    LogoutUser() {
        const body = {}
        return this.http.post(this.rootUrl + '/api/v1/logout/', body);
    }

}