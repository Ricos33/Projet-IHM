#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  PlatformController
#
#  Created by Ingenuity i/o on 2026/01/07
#
#  Copyright © 2025 Ingenuity i/o. All rights reserved.
#
import ingescape as igs


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class PlatformController(metaclass=Singleton):
    def __init__(self):
        # inputs
        self.Available_AssetsI = None
        self.User_ActionI = None
        self.Asset_IdI = None
        self.User_DecisionI = None

        # outputs
        self._TrendO = None
        self._Selected_Asset_CatO = None
        self._Selected_Asset_IdO = None
        self._User_Decision_OutO = None
        self._Start_SimulationO = None
        self._Asset_ActionO = None

    # outputs
    @property
    def TrendO(self):
        return self._TrendO

    @TrendO.setter
    def TrendO(self, value):
        self._TrendO = value
        if self._TrendO is not None:
            igs.output_set_string("Trend", self._TrendO)
    @property
    def Selected_Asset_CatO(self):
        return self._Selected_Asset_CatO

    @Selected_Asset_CatO.setter
    def Selected_Asset_CatO(self, value):
        self._Selected_Asset_CatO = value
        if self._Selected_Asset_CatO is not None:
            igs.output_set_string("Selected_Asset_Cat", self._Selected_Asset_CatO)
    @property
    def Selected_Asset_IdO(self):
        return self._Selected_Asset_IdO

    @Selected_Asset_IdO.setter
    def Selected_Asset_IdO(self, value):
        self._Selected_Asset_IdO = value
        if self._Selected_Asset_IdO is not None:
            igs.output_set_string("Selected_Asset_ID", self._Selected_Asset_IdO)
    @property
    def User_Decision_OutO(self):
        return self._User_Decision_OutO

    @User_Decision_OutO.setter
    def User_Decision_OutO(self, value):
        self._User_Decision_OutO = value
        if self._User_Decision_OutO is not None:
            igs.output_set_bool("User_Decision_Out", self._User_Decision_OutO)
    @property
    def Start_SimulationO(self):
        return self._Start_SimulationO

    @Start_SimulationO.setter
    def Start_SimulationO(self, value):
        self._Start_SimulationO = value
        if self._Start_SimulationO is not None:
            igs.output_set_bool("Start_Simulation", self._Start_SimulationO)
    @property
    def Asset_ActionO(self):
        return self._Asset_ActionO

    @Asset_ActionO.setter
    def Asset_ActionO(self, value):
        self._Asset_ActionO = value
        if self._Asset_ActionO is not None:
            igs.output_set_string("Asset_Action", self._Asset_ActionO)


