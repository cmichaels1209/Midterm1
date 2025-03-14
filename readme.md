##  Design Patterns Used

1. **Singleton Pattern** - Ensures only one instance of the calculator history manager exists.  
   - **Implementation:** [history_manager.py](https://github.com/cmichaels1209/Midterm1/blob/main/app/history_manager.py)

2. **Factory Method** - Creates calculator operations dynamically based on user input.  
   - **Implementation:** [operation_factory.py](https://github.com/cmichaels1209/homework6/blob/main/app/operation_factory.py)

3. **Command Pattern** - Encapsulates each calculator operation as an object to enable history tracking and undo functionality.  
   - **Implementation:** [commands.py](https://github.com/cmichaels1209/homework6/blob/main/app/commands.py)

##  Environment Variables Usage
This project uses environment variables to configure logging levels dynamically.

### How it Works:
- The logging level is set based on the `LOG_LEVEL` environment variable.
- Users can change logging verbosity by setting:
  ```bash
  export LOG_LEVEL=DEBUG  # Enable detailed logs
Implementation Code Reference: logging_config.py

 EAFP (Easier to Ask for Forgiveness than Permission)
Used when retrieving environment variables; assumes they exist and handles KeyError if missing.

## 🎥 Video Demonstration
Watch a 3-minute walkthrough of this project, covering key features and functionality:

▶️ **[Video Link](https://youtu.be/example-link)**
