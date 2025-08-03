CSS = """
    Screen {
        align: center bottom;
        background:  $surface;
        color: white;
        border: none;
    }

    .menu-title {
    background: transparent;
    color: #E0E6ED;
    border: round #7B68EE;
    }

    
    #id:hover {
        background: #7B68EE;

    }
        
    #grade_bar {
    
        background: $surface;
        color: white;
        border: none;

    }
    
    .centered-menu {
    align: center bottom;
    width: 100%;
    align-horizontal: center;
    background: transparent;
    color: green;

    }

    #file_select {
        background: $background; /* or a hex like #222 */
        color: white;
        border: solid green; /* Change to match your theme */
        
    }

    #file_select:focus {
        border: solid yellow;
        background: #111; /* Different when focused */
    }

    #file_select > .prompt {
        color: gray; /* Custom prompt color */
    }

    /* Optional: tweak dropdown item styles */
    #file_select > .option--selected {
        background: darkgreen;
        color: white;
    }
            
    .start-btn {
        margin: 2 2;
        align: center middle;
        width: 100%;
        padding: 1 2;

    }

    .start-btn:hover {
        background:#7B68EE;
        color: #FFFFFF;

    }


    /* Base Buttons */
    Button {
        margin: 1 2;
        width: 100%;
        padding: 1 1;
        background: transparent;
        color: white;
        border: none;
        text-style: bold;
        
    }

    Button:hover {
        background: #3B82F6;
        color: #FFFFFF;
        border: round none ;
    }

    /* Static Boxes */
    Static {
        color: #E0E6ED;
        background: transparent;
        border: transparent;
        padding: 1 2;
        width: 100%;
        height: auto;
        text-style: bold;
    }

    Static:hover {
        background: #7B68EE;
        color: #FFFFFF;
        border: none ;

    }

    /* Summary Panel */
    Static#summary_box {
        width: 100%;
        padding: 1 2;
        border: none;
        background: transparent;
        
    }


    

    /* Edit Button */
    .edit-btn {
        background: #1E293B;
        width: 85%;
        color: #E0E6ED;
        padding: 1 2;
        border: round #3B82F6;
        text-style: bold;
        margin: 1;
    }

    .edit-btn:hover {
        background: #2563EB;
        color: #FFFFFF;
        border: round #93C5FD;
    }

    /* Save Button */
    .save-btn {
        background: #1E293B;
        width: 100%;
        color: #E0E6ED;
        padding: 1 2;
        border: round #3B82F6;
        text-style: bold;
        margin: 1;
    }

    /* Scrollable Course List */
    #course_list {
        width: 4fr;
        height: 100%;
        overflow: auto;
        padding: 1;
        border: none;
        background: transparent;
    }

    .file-item {
        padding: 1 1;
        background: transparent;
        color: white;
        border: none;
    }  

    /* Course Boxes */
    .course-box {
    border: none; /* or use a subtle border if you prefer */
    padding: 0 1;
    margin: 1;
    width: 100%;
    height: auto;
    content-align: left middle;
    background: transparent;
    color: #E0E6ED;  /* Light floating text */
    text-style: bold;
}

    /* Completed Courses */
    .course-box.completed {
        border: none;
        color: #10B981; /* Mint green floating text */
        background: transparent;
    }

    /* Pending Courses */
    .course-box.pending {
        border: none;
        color: #8B5CF6; /* Lavender/purple floating text */
        background: transparent;
    }

    DataTable {
    background: $surface;
    color: $text;
    border: none;
    scrollbar-background: transparent;
    scrollbar-color: transparent;

    }

    .summary-container {
        scrollbar-background: transparent;
        scrollbar-color: transparent;
        background: transparent;

    }
            
    LoadingIndicator {
        color: #7B68EE;
        width: 100%;    
    }

  

    Switch {
        height: auto;
        width: auto;
        border:  round #7B68EE;
        background:$surface;
        
        
    }

    Switch > .switch--knob {
    background: #7B68EE;
             
    }

    Switch > .switch--track {
    background: #7B68EE;
    border: #7B68EE;
    
    }

    Switch > .switch--slider {
    color: #7B68EE;
    background: $surface;
    
    }

    .switch-label {
        height: 3;
        content-align: center middle;
        width: auto; 
        background:transparent;
        color: #ffffff     
                    
    }
    
    #time-display {
    dock: top;
    content-align: center middle;
    padding: 1 4;
    }

    #time-display:hover {
    background:transparent;
    border: round white;

    }



    #stop-botton {
    display:none;
    color: white;
    text-style: bold;
    background: black;
    content-align: center middle;

    }

    #start-botton {
    background: white;
    color: #7B68EE;
    text-style: bold;
    content-align: center middle;
    }

    .started #start-botton {
    display: none;
    }

    .started #stop-botton {
    display: block;
    }



    #center_container {
    height: 100%;
    width: 100%;  
    align: center middle;
    color: $text;
    background:$surface;       
    }
    
    #ejemplo {
        color: white;
        border: none;
        background: $surface;
        padding: 0 1;
        margin: 1 0;
        height: auto;
        align: center bottom ;

        
    }
    

    Center {
    margin-top: 1;
    margin-bottom: 1;
    layout: horizontal;
    }

    Container {
    overflow: hidden hidden;
    height: auto;
    }
    

    Bar > .bar--indeterminate {
    color: white;
    background: transparent;
    }

    Bar:hover{
    background:transparent;
    color:transparent;
    }

    RecordingScreen #record-bar:hover{
    background:transparent;
    border:white;

    }

    #record-bar {
    padding:1;
    }



    Bar > .bar--bar {
        color: #7B68EE;
        background: transparent;
        width:100%
    }

    Bar > .bar--complete {
        color: $error;
    }

    PercentageStatus {
        text-style: reverse;
        color: $secondary;
    }

    ETAStatus {
        text-style: underline;
    }



    Select {
    width: 60;
    height: 30;
    margin: 1 2;
    align: center top;
    background: transparent;
    color: transparent;
    border: round black;

    }

    Select > Option:hover{
    background: transparent;
    color:transparent;
    }

    Select:focus {
    border: transparent;
    background: transparent;
    }


    Select > Option {
    background: transparent;
    color: transparent;
    }

    Select > Option:nocolor {
    background: transparent;
    color: transparent;
    }    


    #target_date {
    border: black;
    color: white;
    align: center bottom ;
    margin: 1 0;

    }

  
    
    

    """