from opentrons import protocol_api
import numpy as np

# metadata
metadata = {
    'protocolName': 'Bradford Platting. V.001',
    'author': 'Alex Perkins',
    'email': 'a.j.p.perkins@sms.ed.ac.uk',
    'description': 'Simple protocol to plate a bradford assay - not dynamic',
    'apiLevel': '2.11'
}






# protocol run function. the part after the colon lets your editor know
# where to look for autocomplete suggestions
def run(protocol: protocol_api.ProtocolContext):

    # labware
    plate = protocol.load_labware('corning_96_wellplate_360ul_flat', '5')

    reagent_falcon_block = protocol.load_labware('trevor_6_tuberack_50000ul','8')
    reagent_2ml_eppendorfs = protocol.load_labware('opentrons_24_tuberack_eppendorf_2ml_safelock_snapcap', '6')
    BSA_standards_2ml_eppendorfs = protocol.load_labware('opentrons_24_tuberack_eppendorf_2ml_safelock_snapcap', '4')


    # pipettes
    tiprack_20ul = protocol.load_labware('opentrons_96_tiprack_20ul', '9')
    left_pipette = protocol.load_instrument(
         'p20_single_gen2', 'left', tip_racks=[tiprack_20ul])

    tiprack_300ul = protocol.load_labware('opentrons_96_tiprack_300ul', '11')
    right_pipette = protocol.load_instrument('p300_single_gen2', 'right', tip_racks=[tiprack_300ul])


    # Commands

     # first laydown the stock-30
    def distribute_stock_30(well, aspirate_height, dispense_volume):

        if dispense_volume == 0:
            pass

        else:
            aspirate_volume = dispense_volume + 20

            right_pipette.well_bottom_clearance.aspirate = aspirate_height
            right_pipette.well_bottom_clearance.dispense = 7

            right_pipette.aspirate(aspirate_volume, reagent_falcon_block['A1'].top(-aspirate_height), rate=0.2)
            protocol.delay(seconds=3)
            right_pipette.touch_tip()

            # Still dispensing 1mm above the bottom
            right_pipette.dispense(dispense_volume, well.top(-29), rate=0.1)
            protocol.delay(seconds=2)
            right_pipette.touch_tip()

            right_pipette.blow_out(reagent_falcon_block['A1'])

     # distribute bradford
    def distribute_bradford(well, aspirate_height, dispense_volume):

        if dispense_volume == 0:
            pass

        else:

            aspirate_volume = dispense_volume

            right_pipette.well_bottom_clearance.aspirate = aspirate_height

            right_pipette.aspirate(aspirate_volume, reagent_falcon_block['A2'].top(-aspirate_height), rate=0.5)
            protocol.delay(seconds=2)
            right_pipette.touch_tip()

            # Still dispensing 1mm above the bottom
            right_pipette.dispense(dispense_volume, well.top(3), rate=0.5)
            protocol.delay(seconds=2)
            right_pipette.move_to(well.top())
            protocol.delay(seconds=2)


    def distribute_protein_mix(aspirate_well, aspirate_plate, dispense_well, dispense_volume):

        if dispense_volume == 0:
            pass

        else:

            left_pipette.pick_up_tip()

            # plus 10%
            aspirate_volume = dispense_volume + (dispense_volume*0.1)

            left_pipette.aspirate(aspirate_volume, aspirate_plate[aspirate_well].bottom(2), rate=0.5)
            protocol.delay(seconds=2)
            left_pipette.touch_tip()

            # Still dispensing 1mm above the bottom
            left_pipette.dispense(dispense_volume, dispense_well.top(-4), rate=0.3)
            protocol.delay(seconds=1)
            left_pipette.touch_tip()

            left_pipette.drop_tip()

    def distribute_standards_mix(aspirate_well, aspirate_plate, dispense_well, dispense_volume):

        if dispense_volume == 0:
            pass

        else:

            left_pipette.pick_up_tip()

            # plus 10%
            aspirate_volume = dispense_volume + (dispense_volume*0.1)

            left_pipette.aspirate(aspirate_volume, aspirate_plate[aspirate_well].bottom(1), rate=0.5)
            protocol.delay(seconds=2)
            left_pipette.touch_tip()

            # Still dispensing 1mm above the bottom
            left_pipette.dispense(dispense_volume, dispense_well.top(-4), rate=0.3)
            protocol.delay(seconds=3)
            left_pipette.touch_tip()

            left_pipette.drop_tip()





    # Dilutions

    dilution_toggle = True
    plate_sample_dilutions = True
    bradford_toggle = True
    plate_standards_toggle = False

    if dilution_toggle:
        ##################################### Dispense stock 30

        stock_30 = np.array([[80, 50, 80, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])

        # flatten array
        stock_30_vols = stock_30.reshape(-1)

        stock_30_aspirate_height = 88.5

        right_pipette.pick_up_tip()

        for well, dispense_vol in zip(reagent_2ml_eppendorfs.wells(), stock_30_vols):

            distribute_stock_30(well, stock_30_aspirate_height, dispense_vol)
            stock_30_aspirate_height = stock_30_aspirate_height + 0.2

        right_pipette.drop_tip()

        ###################################### make 20x and mix

        sample_20x_aspirate_height = 38

        right_pipette.transfer(80,
                                BSA_standards_2ml_eppendorfs.wells_by_name()['A6'].top(-sample_20x_aspirate_height),
                                reagent_2ml_eppendorfs.wells_by_name()['A1'].top(-sample_20x_aspirate_height),
                                new_tip='always',
                                # mix 2 times with 50uL before aspirating
                                mix_before=(5, 60),
                                mix_after=(10,120)
                                )


        ################################## make x40 and mix

        sample_50x_aspirate_height = 38

        right_pipette.transfer(50,
                            reagent_2ml_eppendorfs.wells_by_name()['A1'].top(-sample_50x_aspirate_height),
                            reagent_2ml_eppendorfs.wells_by_name()['B1'].top(-sample_50x_aspirate_height),
                            new_tip='always',
                            # mix 2 times with 50uL before aspirating
                            mix_before=(3, 100),
                            mix_after=(10,60)
                            )

        ################################## make x100 and mix

        sample_50x_aspirate_height = 38

        right_pipette.transfer(20,
                            reagent_2ml_eppendorfs.wells_by_name()['A1'].top(-sample_50x_aspirate_height),
                            reagent_2ml_eppendorfs.wells_by_name()['C1'].top(-sample_50x_aspirate_height),
                            new_tip='always',
                            # mix 2 times with 50uL before aspirating
                            mix_before=(3, 80),
                            mix_after=(10,60)
                            )
        ################################## make x250 and mix

        #sample_50x_aspirate_height = 35

        #right_pipette.transfer(50,
        #                    reagent_2ml_eppendorfs.wells_by_name()['A1'].top(-sample_50x_aspirate_height),
        #                    reagent_2ml_eppendorfs.wells_by_name()['C1'].top(-sample_50x_aspirate_height),
        #                    new_tip='always',
        #                    # mix 2 times with 50uL before aspirating
        #                    mix_before=(3, 50),
        #                    mix_after=(10,220)
        #                    )

        ################################## make x400 and mix
        #sample_50x_aspirate_height = 35
        #right_pipette.transfer(50,
        #                    reagent_2ml_eppendorfs.wells_by_name()['B1'].top(-sample_50x_aspirate_height),
        #                    reagent_2ml_eppendorfs.wells_by_name()['D1'].top(-sample_50x_aspirate_height),
        #                    new_tip='always',
        #                    # mix 2 times with 50uL before aspirating
        #                    mix_before=(3, 50),
        #                    mix_after=(10,170)
        #                    )

        ################################## make x500 and mix
        #sample_50x_aspirate_height = 35
        #right_pipette.transfer(30,
        #                    reagent_2ml_eppendorfs.wells_by_name()['B1'].top(-sample_50x_aspirate_height),
        #                    reagent_2ml_eppendorfs.wells_by_name()['A2'].top(-sample_50x_aspirate_height),
        #                    new_tip='always',
        #                    # mix 2 times with 50uL before aspirating
        #                    mix_before=(3, 50),
        #                    mix_after=(10,130)
        #                    )


        ################################## make x600 and mix
        #sample_50x_aspirate_height = 35
        #right_pipette.transfer(30,
        #                    reagent_2ml_eppendorfs.wells_by_name()['B1'].top(-sample_50x_aspirate_height),
        #                    reagent_2ml_eppendorfs.wells_by_name()['B2'].top(-sample_50x_aspirate_height),
        #                    new_tip='always',
        #                    # mix 2 times with 50uL before aspirating
        #                    mix_before=(3, 50),
        #                    mix_after=(10,140)
        #                    )

        ################################## make x750 and mix
        #sample_50x_aspirate_height = 35
        #right_pipette.transfer(50,
        #                    reagent_2ml_eppendorfs.wells_by_name()['C1'].top(-sample_50x_aspirate_height),
        #                    reagent_2ml_eppendorfs.wells_by_name()['C2'].top(-sample_50x_aspirate_height),
        #                    new_tip='always',
        #                    # mix 2 times with 50uL before aspirating
        #                    mix_before=(3, 50),
        #                    mix_after=(10,130)
        #                    )


        ################################## make x1000 and mix
        #sample_50x_aspirate_height = 35
        #right_pipette.transfer(30,
        #                    reagent_2ml_eppendorfs.wells_by_name()['B2'].top(-sample_50x_aspirate_height),
        #                    reagent_2ml_eppendorfs.wells_by_name()['D2'].top(-sample_50x_aspirate_height),
        #                    new_tip='always',
        #                    # mix 2 times with 50uL before aspirating
        #                    mix_before=(3, 50),
        #                    mix_after=(8,130)
        #                    )


    ################################## plate Bradford reagent

    if bradford_toggle:

        bradford_arr = np.array([
                                [300, 300, 300, 0, 0, 0, 0, 0],
                                [300, 300, 300, 0, 0, 0, 0, 0],
                                [300, 300, 300, 0, 0, 0, 0, 0],

                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],

                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0]

                                #[300, 300, 300, 300, 300, 300, 300, 300],
                                #[300, 300, 300, 300, 300, 300, 300, 300],
                                #[300, 300, 300, 300, 300, 300, 300, 300],
                                #[300, 300, 300, 300, 300, 300, 300, 300],
                                #[300, 300, 300, 300, 300, 300, 300, 300]
                                ])

        # flatten array
        bradford_arr = bradford_arr.reshape(-1)

        # initial aspiriation height for initial volume of 22.5ml of bradford
        bradford_aspirate_height = 62

        right_pipette.pick_up_tip()

        for well, dispense_vol in zip(plate.wells(), bradford_arr):

            distribute_bradford(well, bradford_aspirate_height, dispense_vol)

            #### unsure about correct descent speed.
            bradford_aspirate_height = bradford_aspirate_height + 0.5

        right_pipette.drop_tip()



    ################################## plate standards

    if plate_standards_toggle:

        asp_wells = ['A1', 'B1', 'C1', 'D1', 'A2', 'B2', 'C2', 'D2']
        disp_rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

        disp_vols = [0, 0, 0, 0, 0, 0, 0, 10, 10, 10, 10, 10]

        aspirate_plate = BSA_standards_2ml_eppendorfs



        for aspirate_well, dispense_row in zip(asp_wells, disp_rows):

            for dispense_well, dispense_volume in zip(plate.rows_by_name()[dispense_row], disp_vols):

                distribute_standards_mix(aspirate_well, aspirate_plate, dispense_well, dispense_volume)


        #############################################################################

    ################################## plate dilutions #1

    if plate_sample_dilutions:

        asp_wells = ['A1', 'B1', 'C1']
        disp_rows = ['A', 'B', 'C']

        disp_vols = [10, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        aspirate_plate = reagent_2ml_eppendorfs

        for aspirate_well, dispense_row in zip(asp_wells, disp_rows):

            for dispense_well, dispense_volume in zip(plate.rows_by_name()[dispense_row], disp_vols):

                distribute_protein_mix(aspirate_well, aspirate_plate, dispense_well, dispense_volume)
