#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  MarketSimulator
#
#  Created by Ingenuity i/o on 2026/01/09
#
#  Copyright © 2025 Ingenuity i/o. All rights reserved.
#
import ingescape as igs
import matplotlib.pyplot as plt
import time

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class MarketSimulator(metaclass=Singleton):
    def __init__(self):
        # inputs
        self.Future_PricesI = None
        self.History_PricesI = None
        self.User_DecisionI = None

        # outputs
        self._Current_PriceO = None
        self._Time_IndexO = None
        self._Decision_ResultO = None

    # outputs
    @property
    def Current_PriceO(self):
        return self._Current_PriceO

    @Current_PriceO.setter
    def Current_PriceO(self, value):
        self._Current_PriceO = value
        if self._Current_PriceO is not None:
            igs.output_set_double("Current_Price", self._Current_PriceO)
    @property
    def Time_IndexO(self):
        return self._Time_IndexO

    @Time_IndexO.setter
    def Time_IndexO(self, value):
        self._Time_IndexO = value
        if self._Time_IndexO is not None:
            igs.output_set_double("Time_Index", self._Time_IndexO)
    @property
    def Decision_ResultO(self):
        return self._Decision_ResultO

    @Decision_ResultO.setter
    def Decision_ResultO(self, value):
        self._Decision_ResultO = value
        if self._Decision_ResultO is not None:
            igs.output_set_string("Decision_Result", self._Decision_ResultO)
    def set_Simulation_DoneO(self):
        igs.output_set_impulsion("Simulation_Done")
    
    
    def run_simulation_plot(self, total_future_duration=5):
        history_prices = self.History_PricesI
        future_prices  = self.Future_PricesI

        if not history_prices or not future_prices:
            print("[MarketSimulator] Missing prices: cannot start simulation")
            return

        history_steps = len(history_prices) - 1
        future_steps = len(future_prices) - 1
        start_price = history_prices[-1]

        all_prices = history_prices + future_prices
        min_price = min(all_prices) - 1
        max_price = max(all_prices) + 1

        decision = self.User_DecisionI


        history_times = list(range(-history_steps, 1))
        delay = total_future_duration / max(1, future_steps)

        plt.ion()
        fig, ax = plt.subplots(figsize=(11, 5))
        ax.set_title("Price Simulation (Preview + Live)")
        ax.set_xlabel("Time")
        ax.set_ylabel("Price")

        ax.set_xlim(-history_steps, future_steps)
        ax.set_ylim(min_price, max_price)
        ax.grid(True)

        ax.axhline(start_price, color='gray', linestyle='--')
        ax.plot(history_times, history_prices, color="blue")

        anim_times = [0]
        anim_prices = [start_price]
        line, = ax.plot(anim_times, anim_prices, color="green")

        text_status = fig.text(0.82, 0.12, "", fontsize=12, ha="left", va="center")

        plt.draw()
        plt.pause(0.0001)

        start = time.time()

        for i in range(1, future_steps + 1):
            new_p = future_prices[i]

            anim_times.append(i)
            anim_prices.append(new_p)

            line.set_xdata(anim_times)
            line.set_ydata(anim_prices)

            color = "green" if new_p >= start_price else "red"
            line.set_color(color)

            abs_gain = new_p - start_price
            pct_gain = (abs_gain / start_price) * 100

            text_status.set_text(f"{abs_gain:+.2f}\n{pct_gain:+.2f}%")
            text_status.set_color(color)

            # publier outputs Ingescape (optionnel mais utile)
            self.Current_PriceO = float(new_p)
            self.Time_IndexO = float(i)

            plt.draw()
            plt.pause(0.00001)

            elapsed = time.time() - start
            expected = i * delay
            if expected > elapsed:
                time.sleep(expected - elapsed)
        
        end_price = future_prices[-1]

        if decision == "BUY":
            if  end_price >= start_price:
                self.Decision_ResultO = "YOU WON " + str(pct_gain) + " %"
            elif end_price < start_price:
                self.Decision_ResultO = "YOU LOST " + str(-pct_gain) + " %"
        elif decision == "SELL":
            if end_price <= start_price:
                self.Decision_ResultO = "YOU WON " + str(-pct_gain) + " %"
            elif end_price > start_price:
                self.Decision_ResultO = "YOU LOST " + str(pct_gain) + " %"
        else:
            self.Decision_ResultO = "YOU FORGOT YOUR DECISION TO BUY OR SELL"

        self.set_Simulation_DoneO()
        plt.ioff() 
        plt.show()



