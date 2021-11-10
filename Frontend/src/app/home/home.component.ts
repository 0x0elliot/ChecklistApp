import { Component, Input, Output, OnInit, EventEmitter } from '@angular/core';
import { TaskService } from '../shared/task.service';
import { Router } from '@angular/router';
import { AuthService } from '../shared/authentication.service';
import { UserService } from '../shared/user.service';
import { HttpErrorResponse } from '@angular/common/http';


@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css'],
  providers : [TaskService, AuthService,UserService]
})
export class HomeComponent implements OnInit {
  @Input() task: Task;
  @Output() onToggleReminder: EventEmitter<Task> = new EventEmitter();

  tasks : any[] = []

  constructor(private taskService : TaskService, private authService : AuthService, private router : Router, private userService : UserService) { }

  ngOnInit(): void {
    console.log(this.authService.getToken())
    if (!this.authService.getToken()) {
      this.router.navigate(["/login"]);
    }

    this.taskService.fetchTasks().subscribe(
      (data : any) => {
        this.tasks = JSON.parse(JSON.stringify(data));
        }
    )
  }

  logout() {
    this.userService.LogoutUser().subscribe((data : any)=>{
      this.authService.destroyToken();
    },
  
   (err : HttpErrorResponse)=>{
     console.log(err);
   });
  }

  AddTask(task_name) {
    this.taskService.addTask(task_name).subscribe((data : any) => {
      window.location.reload();
    }
    );
  }

  DeleteTask(task_id) {
    this.taskService.deleteTask(task_id).subscribe((data : any) => {
      window.location.reload();
    }
    );
  }

}
