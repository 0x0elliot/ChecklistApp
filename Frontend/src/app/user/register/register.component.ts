import { Component, OnInit } from '@angular/core';
import { NgForm } from '@angular/forms';
import { UserService } from 'src/app/shared/user.service';
import { HttpErrorResponse } from '@angular/common/http';


@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css'],
  providers: [
    UserService,
  ]
})
export class RegisterComponent implements OnInit {

  isRegisterError : boolean = false;
  isRegisterSuccess : boolean = false;

  constructor(private userService : UserService) { }

  ngOnInit(): void {
  }

  OnSubmitRegister(Name, Email, Password){
    this.userService.registerUser(Name, Email, Password).subscribe((data : any) => {
      this.isRegisterSuccess = true;
    },

    (err : HttpErrorResponse)=>{
      this.isRegisterError = true;
    });
  }
}