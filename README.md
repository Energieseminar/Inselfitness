# Energy Seminar Monitoring System

Welcome to the Github repository for the Energy Seminar Monitoring System! This project focuses on monitoring and analyzing the performance of a unique off-grid energy system located on the tower of the Energy Technology Institute at the Technical University of Berlin.

## Project Overview

The off-grid system consists of four solar modules, a small wind turbine (KWEA), a power supply, a control cabinet with measurement technology, a lead-acid battery, and on the consumer side, two computers and an outlet form the island setup of the Energy Seminar.

For a visual introduction, check out our [YouTube video](https://www.youtube.com/watch?v=x9bFlDJO12g).

The primary goals of this project are to conduct research on demand-oriented power supply through renewable energy sources in isolated systems. The system includes components such as:

- Small wind turbine and four photovoltaic modules as generation units.
- Power supply acting as a "virtual biogas plant" to balance power from the grid.
- Solar accumulators for load balancing.
- Real consumer system (computers and outlets in the Energy Seminar office).

## Components and Technologies

### Photovoltaic System

The generator unit comprises a KWEA and four Soltronic "SolHp 50-12S" PV modules, each with 50 Wpeak power. The modules are connected in series to achieve the required system voltage of approximately 24 V, regulated by a charge controller.

### Small Wind Turbine (KWEA)

The Air-X, a low-friction brushless permanent magnet generator, serves as the small wind turbine. It includes a microprocessor and a voltage regulator, optimizing power output based on wind speed. The voltage regulator ensures that the system voltage is maintained within the desired range.

### Power Supply and Energy Storage

A "virtual biogas plant" power supply is configured to start at a critical system voltage of 23.8 Volts, providing necessary regulation. The energy storage consists of two sealed lead-acid batteries, each with a voltage of 12 Volts and a capacity of 90 Ampere-hours, forming a 24 Volt system. Excess energy is stored, and when needed, the stored energy is released to meet demand.

### Interconnections and Inverter

All generation units, the power supply, and the energy storage are interconnected in a control cabinet. The inverter, a "STECA SOLARIX PI-1100," converts the 24 Volt DC to 230 Volt AC, supplying power to a computer in the Energy Seminar office.

## Monitoring and Safety Features

To analyze system utilization and the impact of storage, a comprehensive measurement system with sensors and an Arduino is integrated. Data is processed using the emoncms software, and a Raspberry Pi displays the information on a screen in the Energy Technology building.

Safety features include a 4 Ampere fuse and an FI circuit breaker for personnel protection. In case of a central network shutdown, a safety relay disconnects the office supply. A transfer switch in the office prevents data loss by seamlessly switching to grid power during system disruptions.

## Raspberry Pi and Arduino

### What is Raspberry Pi?

-A Raspberry Pi is a small, single-board computer developed by the Raspberry Pi Foundation in the United Kingdom. It is designed to be a low-cost, credit-card-sized computer that plugs into a computer monitor or TV, and it uses a standard keyboard and mouse. 

### What is Arduino?

-Arduino is an open-source platform used for building electronics projects. Arduino consists of both a physical programmable circuit board (often referred to as a microcontroller) and a piece of software, or IDE (Integrated Development Environment) that runs on your computer, used to write and upload computer code to the physical board.

### Raspberry Pi and Arduino in serial connection

-To get started, connect your Arduino to your computer, so you can upload the code into the board. After that, connect the USB cable to the Raspberry Pi. The Raspberry Pi will power the Arduino via this cable. To make a Serial connection you can also use plain wires between the Raspberry Pi GPIOs and the Arduino pins

### Video Links

Getting started with Raspberry Pi and Arduino: https://youtu.be/xc9rUI0F6Iw?si=9YZu60pkYA3Ehoic


Serial Connection between Raspberry Pi and Arduino: https://youtu.be/jU_b8WBTUew?si=bmbPZzC8YB6uMPUu




For more insights, explore our [YouTube channel](https://www.youtube.com/channel/your-channel).

Feel free to contribute to this open-source project and be part of advancing sustainable energy solutions!
