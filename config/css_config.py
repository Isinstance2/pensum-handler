CSS = """
    Screen {
        align: center bottom;
        background:  $surface;
        color: transparent;
    }

    .menu-title {
    background: transparent;
    color: #E0E6ED;
    border: round #10B981;
    }

    .centered-menu {
    align: center bottom;
    width: 100%;
    align-horizontal: center;
    background: transparent;
    color: transparent;

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
        background: #10B981;
        color: #FFFFFF;
        border: round none ;
    }

    /* Static Boxes */
    Static {
        color: #E0E6ED;
        background: #1E222A;
        border: round #1F2937;
        padding: 1 2;
        width: 100%;
        height: auto;
        text-style: bold;
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
        color: green;
        width: 100%;    
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
    



    Select {
    width: 60;
    height: 30;
    margin: 1 2;
    align: center top;
    background: transparent;
    color: green;
    border: none;

    }

    #target_date {
    border: black;
    color: white;
    align: center bottom ;
    margin: 1 0;

    }

  
    
    

    """