#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  MarketSimulator
#
#  Created by Ingenuity i/o on 2026/01/09
#
#  Copyright © 2025 Ingenuity i/o. All rights reserved.
#

import json
import signal
import getopt
import time
from pathlib import Path
import traceback
import sys

from MarketSimulator import *


port = 5670
agent_name = "MarketSimulator"
device = None
verbose = False
is_interrupted = False
start_simulation = False
prices_ready = False


short_flag = "hvip:d:n:"
long_flag = ["help", "verbose", "interactive_loop", "port=", "device=", "name="]

ingescape_path = Path("~/Documents/Ingescape").expanduser()


def print_usage():
    print("Usage example: ", agent_name, " --verbose --port 5670 --device device_name")
    print("\nthese parameters have default value (indicated here above):")
    print("--verbose : enable verbose mode in the application (default is disabled)")
    print("--port port_number : port used for autodiscovery between agents (default: 31520)")
    print("--device device_name : name of the network device to be used (useful if several devices available)")
    print("--name agent_name : published name for this agent (default: ", agent_name, ")")
    print("--interactive_loop : enables interactive loop to pass commands in CLI (default: false)")


def print_usage_help():
    print("Available commands in the terminal:")
    print("	/quit : quits the agent")
    print("	/help : displays this message")

def return_io_value_type_as_str(value_type):
    if value_type == igs.INTEGER_T:
        return "Integer"
    elif value_type == igs.DOUBLE_T:
        return "Double"
    elif value_type == igs.BOOL_T:
        return "Bool"
    elif value_type == igs.STRING_T:
        return "String"
    elif value_type == igs.IMPULSION_T:
        return "Impulsion"
    elif value_type == igs.DATA_T:
        return "Data"
    else:
        return "Unknown"

def return_event_type_as_str(event_type):
    if event_type == igs.PEER_ENTERED:
        return "PEER_ENTERED"
    elif event_type == igs.PEER_EXITED:
        return "PEER_EXITED"
    elif event_type == igs.AGENT_ENTERED:
        return "AGENT_ENTERED"
    elif event_type == igs.AGENT_UPDATED_DEFINITION:
        return "AGENT_UPDATED_DEFINITION"
    elif event_type == igs.AGENT_KNOWS_US:
        return "AGENT_KNOWS_US"
    elif event_type == igs.AGENT_EXITED:
        return "AGENT_EXITED"
    elif event_type == igs.AGENT_UPDATED_MAPPING:
        return "AGENT_UPDATED_MAPPING"
    elif event_type == igs.AGENT_WON_ELECTION:
        return "AGENT_WON_ELECTION"
    elif event_type == igs.AGENT_LOST_ELECTION:
        return "AGENT_LOST_ELECTION"
    else:
        return "UNKNOWN"

def signal_handler(signal_received, frame):
    global is_interrupted
    print("\n", signal.strsignal(signal_received), sep="")
    is_interrupted = True


def on_agent_event_callback(event, uuid, name, event_data, my_data):
    try:
        agent_object = my_data
        assert isinstance(agent_object, MarketSimulator)
        # add code here if needed
    except:
        print(traceback.format_exc())



# inputs
def History_Prices_input_callback(io_type, name, value_type, value, my_data):
    try:
        agent_object = my_data
        assert isinstance(agent_object, MarketSimulator)

        history_prices = json.loads(value.decode("utf-8"))
        agent_object.History_PricesI = history_prices
        print(f"[MarketSimulator] History_Prices received ({len(history_prices)} pts)")

    except:
        print(traceback.format_exc())

def Future_Prices_input_callback(io_type, name, value_type, value, my_data):
    try:
        agent_object = my_data
        assert isinstance(agent_object, MarketSimulator)

        future_prices = json.loads(value.decode("utf-8"))
        agent_object.Future_PricesI = future_prices
        print(f"[MarketSimulator] Future_Prices received ({len(future_prices)} pts)")

    except:
        print(traceback.format_exc())


def Start_Simulation_input_callback(io_type, name, value_type, value, my_data):
    try:
        agent_object = my_data
        assert isinstance(agent_object, MarketSimulator)
        global start_simulation
        print("[MarketSimulator] Start_Simulation received")
        start_simulation = True
            
    except:
        print(traceback.format_exc())

def User_Decision_input_callback(io_type, name, value_type, value, my_data):
    try:
        agent_object = my_data
        assert isinstance(agent_object, MarketSimulator)
        agent_object.User_DecisionI = value
        # add code here if needed
    except:
        print(traceback.format_exc())

if __name__ == "__main__":

    # catch SIGINT handler before starting agent
    signal.signal(signal.SIGINT, signal_handler)
    interactive_loop = False

    try:
        opts, args = getopt.getopt(sys.argv[1:], short_flag, long_flag)
    except getopt.GetoptError as err:
        igs.error(err)
        sys.exit(2)
    for o, a in opts:
        if o == "-h" or o == "--help":
            print_usage()
            exit(0)
        elif o == "-v" or o == "--verbose":
            verbose = True
        elif o == "-i" or o == "--interactive_loop":
            interactive_loop = True
        elif o == "-p" or o == "--port":
            port = int(a)
        elif o == "-d" or o == "--device":
            device = a
        elif o == "-n" or o == "--name":
            agent_name = a
        else:
            assert False, "unhandled option"

    igs.agent_set_name(agent_name)
    igs.definition_set_class("MarketSimulator")
    igs.definition_set_package("Agents")
    igs.log_set_console(verbose)
    igs.log_set_file(True, None)
    igs.log_set_stream(verbose)
    igs.set_command_line(sys.executable + " " + " ".join(sys.argv))

    igs.debug(f"Ingescape version: {igs.version()} (protocol v{igs.protocol()})")

    if device is None:
        # we have no device to start with: try to find one
        list_devices = igs.net_devices_list()
        list_addresses = igs.net_addresses_list()
        if len(list_devices) == 1:
            device = list_devices[0]
            igs.info("using %s as default network device (this is the only one available)" % str(device))
        elif len(list_devices) == 2 and (list_addresses[0] == "127.0.0.1" or list_addresses[1] == "127.0.0.1"):
            if list_addresses[0] == "127.0.0.1":
                device = list_devices[1]
            else:
                device = list_devices[0]
            print("using %s as de fault network device (this is the only one available that is not the loopback)" % str(device))
        else:
            if len(list_devices) == 0:
                igs.error("No network device found: aborting.")
            else:
                igs.error("No network device passed as command line parameter and several are available.")
                print("Please use one of these network devices:")
                for device in list_devices:
                    print("	", device)
                print_usage()
            exit(1)

    agent = MarketSimulator()

    igs.observe_agent_events(on_agent_event_callback, agent)

    igs.input_create("Future_Prices", igs.DATA_T, None)
    igs.observe_input("Future_Prices", Future_Prices_input_callback, agent)
    igs.input_create("History_Prices", igs.DATA_T, None)
    igs.observe_input("History_Prices", History_Prices_input_callback, agent)
    igs.input_create("Start_Simulation", igs.IMPULSION_T, None)
    igs.observe_input("Start_Simulation", Start_Simulation_input_callback, agent)
    igs.input_create("User_Decision", igs.STRING_T, None)
    igs.observe_input("User_Decision", User_Decision_input_callback, agent)

    igs.output_create("Current_Price", igs.DOUBLE_T, None)
    igs.output_create("Time_Index", igs.DOUBLE_T, None)
    igs.output_create("Decision_Result", igs.STRING_T, None)
    igs.output_create("Simulation_Done", igs.IMPULSION_T, None)

    igs.start_with_device(device, port)
    # catch SIGINT handler after starting agent
    signal.signal(signal.SIGINT, signal_handler)

    if interactive_loop:
        print_usage_help()
        while True:
            command = input()
            if command == "/quit":
                break
            elif command == "/help":
                print_usage_help()
    else:
        while (not is_interrupted) and igs.is_started():
            if start_simulation:
                print("[MarketSimulator] Launching simulation")

                start_simulation = False  # reset

                agent.run_simulation_plot()
            time.sleep(0.1)

    igs.stop()
