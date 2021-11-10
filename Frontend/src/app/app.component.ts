import { OnInit, Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  constructor(private router : Router) {}
  title = 'Tracker';

  ngOnInit(): void {
    if (this.router.url == "/") {
      this.router.navigate(['/home'])
    }
  }

}
