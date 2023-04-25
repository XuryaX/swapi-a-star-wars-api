import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { DatasetListComponent } from './dataset-list/dataset-list.component';
import { HttpClientModule } from '@angular/common/http';
import { DatasetDetailsComponent } from './dataset-details/dataset-details.component';
import { InfiniteScrollDirective } from './infinite-scroll.directive';
import { FormsModule } from '@angular/forms';


@NgModule({
  declarations: [
    AppComponent,
    DatasetListComponent,
    DatasetDetailsComponent,
    InfiniteScrollDirective
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    InfiniteScrollDirective,
    HttpClientModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
