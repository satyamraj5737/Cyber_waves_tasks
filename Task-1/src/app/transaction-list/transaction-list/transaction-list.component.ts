import { Component, OnInit } from '@angular/core';
import { StoreDataService } from '../../store-data.service';

@Component({
  selector: 'app-transaction-list',
  templateUrl: './transaction-list.component.html',
  styleUrls: ['./transaction-list.component.scss']
})
export class TransactionListComponent implements OnInit {
  transactions: any[] = [];

  constructor(private storeDataService: StoreDataService) {}

  ngOnInit() {
    this.transactions = this.storeDataService.getData();
  }
}
