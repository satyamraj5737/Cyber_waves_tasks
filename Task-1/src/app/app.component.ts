import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { TransactionFormComponent } from './transaction-form/transaction-form/transaction-form.component';
import { TransactionListComponent } from './transaction-list/transaction-list/transaction-list.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, TransactionFormComponent, TransactionListComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'Task-1';
}
