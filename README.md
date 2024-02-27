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

- The Raspberry Pi Foundation in the UK created the Raspberry Pi, a tiny single-board computer. It is intended to be an inexpensive, credit card-sized computer that connects to a TV or computer monitor and makes use of a regular keyboard and mouse.

### What is Arduino?

- An open-source platform called Arduino is used to construct electronics projects. Arduino is made up of a physical programmable circuit board and an IDE, or integrated development environment, that is installed on your computer and is used to write and upload computer code to the board.

### Raspberry Pi and Arduino in serial connection

- In order to upload the code to the board, first connect your Arduino to your computer. Next, attach the Raspberry Pi to the USB cord. This cable will be used to power the Arduino by the Raspberry Pi. Plain wires can also be used to connect the Raspberry Pi GPIOs and Arduino pins in a serial fashion.

### Video Links

Getting started with Raspberry Pi and Arduino: https://youtu.be/xc9rUI0F6Iw?si=9YZu60pkYA3Ehoic
[Credits: RimstarOrg]

Serial Connection between Raspberry Pi and Arduino: https://youtu.be/jU_b8WBTUew?si=bmbPZzC8YB6uMPUu
[Credits: Robotics Back-End]

## Additional Information


For more insights, explore our [YouTube channel](https://www.youtube.com/channel/your-channel).

Feel free to contribute to this open-source project and be part of advancing sustainable energy solutions!
