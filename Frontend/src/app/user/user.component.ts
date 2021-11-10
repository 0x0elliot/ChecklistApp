import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';


@Component({
  selector: 'app-user',
  templateUrl: './user.component.html',
  styleUrls: ['./user.component.css']
})
export class UserComponent implements OnInit {


  constructor(private router : Router) { }

  logincolor : String;
  registercolor : String;

  ngOnInit(): void {

  this.logincolor = new String("#E0E0E0")
  this.registercolor = new String("#E0E0E0")
    if (this.router.url == "/login") {
      this.logincolor = new String("#E9425F");
    }
    else if (this.router.url == "/register") {
      this.registercolor = new String("#E9425F");
    }
}
}
