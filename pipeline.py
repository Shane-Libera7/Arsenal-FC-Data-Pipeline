import subprocess
import logging
import schedule 
import time 
import sys

#Logging Setup --logogs to both terminal and a Log File 
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', handlers=[logging.FileHandler("pipeline.log"), logging.StreamHandler()])


#Stage Runner 
def run_stage(script, stage_name):
    logging.info(f"Starting {stage_name}...")
    result = subprocess.run(["python3", script], capture_output=True, text=True)
    if result.returncode != 0:
        logging.error(f"{stage_name} failed: {result.stderr}")
        raise Exception(f"{stage_name} failed")
    logging.info(f"{stage_name} complete")
    print(result.stdout)


#Full Pipeline

def run_pipeline():
    try:
        logging.info("Pipeline started")
        run_stage("extract/extract.py", "Extract")
        run_stage("transform/transform.py", "Transform")
        run_stage("load/load.py", "Load")
        logging.info("Pipeline completed successfully")
    except Exception as e:
        logging.error(f"Pipeline failed: {e}")




#Entry Point 
if __name__ == "__main__":
    #Manual Trigger
    if len(sys.argv) > 1 and sys.argv[1] == "--run-now":
        run_pipeline()
    else:
        #Scheduled Trigger
        logging.info("Scheduler started - pipeline runs every Tuesday at 6am")
        schedule.every().tuesday.at("06:00").do(run_pipeline)
        while True:
            schedule.run_pending()
            time.sleep(60)

