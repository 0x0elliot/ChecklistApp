import { Component, OnInit } from '@angular/core';
import { UserService } from 'src/app/shared/user.service';
import { Router } from '@angular/router';
import { HttpErrorResponse } from '@angular/common/http';
import { User } from 'src/app/shared/user.model';
import { HttpClient, HttpHandler } from '@angular/common/http';


@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'],
  providers: [
    UserService,
    HttpClient
  ]
})

export class LoginComponent implements OnInit {
  isLoginError : boolean = false;

  constructor(private userService : UserService, private router : Router) { }

  ngOnInit() : void {
  }

  OnSubmitLogin(Email, Password){
  this.userService.LoginUser(Email, Password).subscribe((data : any)=>{
    window.localStorage.setItem('session', data.authentication_token);
    this.router.navigate(['/home']);
 },

 (err : HttpErrorResponse)=>{
   this.isLoginError = true;
 });
}

}