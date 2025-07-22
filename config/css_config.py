CSS = """
    Screen {
        align: center middle;
        background: black;
        color: #E0E6ED;
    }

    .menu-title {
    background: transparent;
    color: #E0E6ED;
    border: round #10B981;
    }

    .centered-menu {
    align: center top;
    width: 100%;
    align-horizontal: center;
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
    background: transparent;
    color: yellow;
    border: none;
    scrollbar-background: transparent;
    scrollbar-color: transparent;
    }

    """