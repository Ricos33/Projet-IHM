#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  ScenarioGenerator
#
#  Created by Ingenuity i/o on 2026/01/09
#
#  Copyright © 2025 Ingenuity i/o. All rights reserved.
#
import ingescape as igs
import json 
import random


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ScenarioGenerator(metaclass=Singleton):
    def __init__(self):
        # inputs
        self.TrendI = None
        self.Asset_ActionI = None
        self.GenerateI = None
        self.Asset_CategoryI = None
        self.Asset_IdI = None

        # outputs
        self._Future_PricesO = None
        self._History_PricesO = None
        self._Scenario_ReadyO = None

    # outputs
    @property
    def Future_PricesO(self):
        return self._Future_PricesO

    @Future_PricesO.setter
    def Future_PricesO(self, value):
        self._Future_PricesO = value
        if self._Future_PricesO is not None:
            igs.output_set_data("Future_Prices", value)
    @property
    def History_PricesO(self):
        return self._History_PricesO

    @History_PricesO.setter
    def History_PricesO(self, value):
        self._History_PricesO = value
        if self._History_PricesO is not None:
            igs.output_set_data("History_Prices", value)
    @property
    def Scenario_ReadyO(self):
        return self._Scenario_ReadyO

    @Scenario_ReadyO.setter
    def Scenario_ReadyO(self, value):
        self._Scenario_ReadyO = value
        if self._Scenario_ReadyO is not None:
            igs.output_set_bool("Scenario_Ready", self._Scenario_ReadyO)
    
    def generate_scenario(
        self,
        initial_price=100,
        history_steps=35,
        future_steps=200
    ):
        # ----- HISTORIQUE -----
        history_prices = [initial_price]
        price = initial_price

        for _ in range(history_steps):
            price += random.uniform(-1, 1)
            history_prices.append(price)

        start_price = history_prices[-1]

        # ----- FUTUR -----
        future_prices = [start_price]
        price = start_price

        for _ in range(future_steps):
            if self.TrendI == "bull":
                variation = random.uniform(-0.5, 1.5)
            elif self.TrendI == "bear":
                variation = random.uniform(-1.5, 0.5)
            else:
                variation = random.uniform(-1, 1)

            price += variation
            future_prices.append(price)

        # sérialisation JSON
        self.History_PricesO = json.dumps(history_prices).encode("utf-8")
        self.Future_PricesO = json.dumps(future_prices).encode("utf-8")
        self.Scenario_ReadyO = True


