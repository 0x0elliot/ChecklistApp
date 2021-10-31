import { Component, OnInit, Input } from '@angular/core';
import {Task} from '../../Task';
import {TASKS} from '../../mock-tasks';
import { faTimes } from '@fortawesome/free-solid-svg-icons';



@Component({
  selector: 'app-task-items',
  templateUrl: './task-items.component.html',
  styleUrls: ['./task-items.component.css']
})
export class TaskItemsComponent implements OnInit {

  constructor() { }

  @Input() task: Task;
  faTimes = faTimes;

  ngOnInit(): void {}
  onDelete(task) {
    console.log(task)
  }

}
