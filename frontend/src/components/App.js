import React,{ Component } from "react";
import {render} from "react-dom";
import HomePage from "./HomePage";
import LoginPage from "./LoginPage";

export default class App extends Component{
    constructor(props){
        super(props)
    }
    render(){
        return (
        <div>
            <HomePage />
            <LoginPage/>
        </div>
        ) 
    }
}
const appDiv=document.getElementById("app");
render(<App />,appDiv);