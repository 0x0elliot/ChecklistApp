import { Injectable } from "@angular/core";
import { HttpClient, HttpHeaders } from "@angular/common/http";
import { BehaviorSubject } from "rxjs";
import { Router } from "@angular/router";


@Injectable()
export class AuthService {
    constructor(private router : Router) { }
    loggedIn: BehaviorSubject<boolean>

    getToken() : string {
        return window.localStorage['session'];
    }

    saveToken(token : string) {
        window.localStorage['session'] = token;
    }

    destroyToken() {
        window.localStorage.clear();
        //window.localStorage.removeItem['session'];
        this.router.navigate(['/login']);

    }

}