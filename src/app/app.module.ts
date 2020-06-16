import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { ListSpotsComponent } from './list-spots/list-spots.component';
import { HttpClientModule } from '@angular/common/http';
import { ResultatComponent } from './resultat/resultat.component';

@NgModule({
  declarations: [
    AppComponent,
    ListSpotsComponent,
    ResultatComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
