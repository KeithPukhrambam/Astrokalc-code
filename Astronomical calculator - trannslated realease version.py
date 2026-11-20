import os
import math
import sympy as sp
import numpy as np
import scipy as sc
from fastapi.responses import PlainTextResponse
from nicegui import app, ui

def clear():
    os.system('cls'if os.name == 'nt' else 'clear')
def calculate_height(orbit_perimeter: float):
    ans = (orbit_perimeter / (2 * pi)) - 6371000
    return {"height": ans}
def orbit_perimeter_from_height(height: float):
    ans = (height + 6371000) * 2 * pi
    return {"orbit_perimeter": ans}
def speed_from_orbit_perimeter(orbit_perimeter: float, time: float):
    ans = orbit_perimeter / time
    return {"speed": ans}
def time_from_orbit_perimeter(orbit_perimeter: float, speed: float):
    ans = orbit_perimeter / speed
    return {"time": ans}
def fuel_calculation(distance: float, fuel_efficency: float):
    ans = distance / fuel_efficency
    return {"fuel": ans}
def fuel_efficency_from_distance_and_fuel(distance: float, fuel: float):
    ans = distance / fuel
    return {"fuel_efficency": ans}
def distance_from_fuel_and_fuel_efficency(fuel: float, fuel_efficency: float):
    ans = fuel * fuel_efficency
    return {"distance": ans}
def ideal_rocket_equation(isp: float, initial_mass: float, final_mass: float):
    delta_v = isp * 9.81 * math.log(initial_mass / final_mass)
    return {"delta_v": delta_v}
def escape_velocity(gravity: float, radius: float):
    escape_velocity = math.sqrt(2 * gravity * radius)
    return {"escape_velocity": escape_velocity}
def delta_mass(initial_mass: float, final_mass: float):
    delta_mass = initial_mass - final_mass
    return {"delta_mass": delta_mass}
def terminal_velocity(mass: float, gravity: float, drag_coefficient: float, cross_sectional_area: float, phi: float):
    terminal_velocity = math.sqrt((2 * mass * gravity) / (phi * drag_coefficient * cross_sectional_area))
    return {"terminal_velocity": terminal_velocity}
def fall_simulation(height):
        return math.sqrt((2*height)/9.81)
def fall_simulation_advanced(height, cross_sectional_area, drag_coefficient, phi, mass, gravity, time_step, scale_height):
    velocity=0
    time_taken=0
    phi_2=phi
    while height > 0:
        drag=0.5*phi_2*(velocity**2)*drag_coefficient*cross_sectional_area
        acceleration=gravity-drag/mass
        velocity+=acceleration*time_step
        height-=velocity*time_step
        phi_2=phi*math.exp((-1*height)/scale_height)
        time_taken+=time_step
    ui.label(f"The time taken to fall is {time_taken}")
    ui.label(f"The maximum fall speed/impact speed of the rocket is {velocity}")
    ui.link('back to rocket stuff', '/rocket_stuff')
    ui.link('Back to home', '/')
def rocket_maximum_height_advanced(scale_height, phi, drag_coefficient, cross_sectional_area, fuel, burn_rate, thrust, gravity, time_step, dry_mass):
    elasped_time=0
    rocket_velocity=0
    current_mass=dry_mass+fuel
    current_height=0
    phi_2=phi
    while fuel > 0:
        dt=min(time_step, fuel/burn_rate)
        air_resistance=0.5*phi_2*(rocket_velocity**2)*drag_coefficient*cross_sectional_area
        current_mass=dry_mass+fuel
        acceleration=(thrust/current_mass)-gravity-air_resistance/current_mass
        current_height+=rocket_velocity*dt
        phi_2=phi*math.exp((-1*current_height)/scale_height) 
        rocket_velocity+=acceleration*dt
        fuel-=burn_rate*dt
        elasped_time+=dt
    current_mass=dry_mass
    while rocket_velocity > 0:
        air_resistance=0.5*phi_2*(rocket_velocity**2)*drag_coefficient*cross_sectional_area
        acceleration=(-1*gravity)-air_resistance/current_mass
        current_height+=rocket_velocity*time_step
        phi_2=phi*math.exp((-1*current_height)/scale_height)
        rocket_velocity+=acceleration*time_step
        elasped_time+=time_step
    ui.label(f"The maximum height of the rocket is {current_height}")
    ui.label(f"The time taken to reach the maximum height is {elasped_time}")
    ui.link('back to rocket stuff', '/rocket_stuff')
    ui.link('Back to home', '/')
pi=3.14159265358979
@ui.page('/')
def home_page():
    ui.add_body_html(
        '<meta name="description" content="Astronomical calculations and approximations, from beginner satellite and fuel tools to rocket science and basic calculus. Not for learning or professional use.">'
    )
    ui.colors(primary='#8B5CF6', accent='#C084FC')
    ui.label('Astronomical Calculator')
    ui.label("Basic section;")
    ui.button('Satellites', on_click=lambda: ui.navigate.to('/satelites'))
    ui.button("Fuel efficency", on_click=lambda: ui.navigate.to('/fuel_efficency'))
    ui.label("")
    ui.label("Advanced section;")
    ui.button("Satelites advanced (coming soon)", on_click=lambda: ui.notify("I said coming soon"))
    ui.button("Rocket stuff (like fall time and maximum height simulations, ideal rocket equation and more)", on_click=lambda: ui.navigate.to('rocket_stuff'))
    ui.label("")
    ui.label("Calculus section;" )
    ui.button("Basic calculus", on_click=lambda: ui.navigate.to('/basic_calculus'))
    ui.button("Calculus Uses (coming soon)", on_click=lambda: ui.notify("I said coming soon"))
    ui.link("You can also find info on this calculator using this button", '/info')
@ui.page('/satelites')
def satellite_page():
    ui.colors(primary='#8B5CF6', accent='#C084FC')
    ui.label("What do you wish to calculate among:")
    ui.button("Orbit perimeter", on_click=lambda: ui.navigate.to('/satellite-orbit-perimeter'))
    ui.button("Height (above sea level)", on_click=lambda: ui.navigate.to('/satellite-height'))
    ui.button("Speed", on_click=lambda: ui.navigate.to('/satellite-speed'))
    ui.button("Time", on_click=lambda: ui.navigate.to('/satellite-time'))
    ui.link('Back to home', '/')
@ui.page('/satellite-height')
def satellite_height_page():
    ui.colors(primary='#8B5CF6', accent='#C084FC')
    ui.label("Height (above sea level)")
    orbit_perimeter = ui.number("What is the orbit perimeter (in meters)?", value=45000000.0, min=40030174.0, step=100.0)
    ui.button("Calculate", on_click=lambda: calculate_and_display_height(orbit_perimeter.value))
def calculate_and_display_height(orbit_perimeter):
    result = calculate_height(orbit_perimeter)
    ui.label(f"The height of your satellite is {result['height']} meters above sea level")
    ui.link('Back to Satellites', '/satelites')
    ui.link('Back to home', '/')
@ui.page('/satellite-orbit-perimeter')
def satellite_orbit_perimeter_page():
    ui.colors(primary='#8B5CF6', accent='#C084FC')
    ui.label("Orbit Perimeter")
    height = ui.number("What is the height (in meters)?", value=400000.0, min=0.0, step=100.0)
    ui.button("Calculate", on_click=lambda: calculate_and_display_orbit_perimeter(height.value))
def calculate_and_display_orbit_perimeter(height):
    result = orbit_perimeter_from_height(height)
    ui.label(f"The orbit perimeter of your satellite is {result['orbit_perimeter']} meters")
    ui.link('Back to Satellites', '/satelites')
    ui.link('Back to home', '/')
@ui.page('/satellite-speed')
def satellite_speed_page():
    ui.colors(primary='#8B5CF6', accent='#C084FC')
    ui.label("Speed")
    orbit_perimeter = ui.number("What is the orbit perimeter (in meters)?", value=45000000.0, min=40030174.0, step=100.0)
    time = ui.number("What is the time (in seconds)?", value=5400.0, min=1.0, step=1.0)
    ui.button("Calculate", on_click=lambda: calculate_and_display_speed(orbit_perimeter.value, time.value))
def calculate_and_display_speed(orbit_perimeter, time):
    result = speed_from_orbit_perimeter(orbit_perimeter, time)
    ui.label(f"The speed of your satellite is {result['speed']} meters per second")
    ui.link('Back to Satellites', '/satelites')
    ui.link('Back to home', '/')
@ui.page('/satellite-time')
def satellite_time_page():
    ui.colors(primary='#8B5CF6', accent='#C084FC')
    ui.label("Time")
    orbit_perimeter = ui.number("What is the orbit perimeter (in meters)?", value=45000000.0, min=40030174.0, step=100.0)
    speed = ui.number("What is the speed (in meters per second)?", value=8333.33, min=1.0, step=1.0)
    ui.button("Calculate", on_click=lambda: calculate_and_display_time(orbit_perimeter.value, speed.value))
def calculate_and_display_time(orbit_perimeter, speed):
    result = time_from_orbit_perimeter(orbit_perimeter, speed)
    ui.label(f"The time for your satellite to complete the orbit is {result['time']} seconds")
    ui.link('Back to Satellites', '/satelites')
    ui.link('Back to home', '/')
@ui.page('/fuel_efficency')
def fuel_efficency_page():
    ui.colors(primary='#8B5CF6', accent='#C084FC')
    ui.label("What do you wish to calculate among:")
    ui.button("fuel", on_click=lambda: ui.navigate.to('/fuel'))
    ui.button("fuel efficency", on_click=lambda: ui.navigate.to('/fuel_efficency_calculation'))
    ui.button("distance", on_click=lambda: ui.navigate.to('/distance_calculation'))
    ui.link('Back to home', '/')
@ui.page('/fuel')
def fuel_page():
    ui.colors(primary='#8B5CF6', accent='#C084FC')
    distance = ui.number("Distance (in meters)", value=1, min=1, step=1)
    fuel_efficency = ui.number("Fuel efficency (in meters per liter)", value=1, min=1, step=1)
    ui.button("Calculate", on_click=lambda: calculate_and_display_fuel(distance.value, fuel_efficency.value))
def calculate_and_display_fuel(distance, fuel_efficency):
    result = fuel_calculation(distance, fuel_efficency)
    ui.label(f"The amount of fuel required is {result['fuel']} liters")
    ui.link('Back to Fuel Efficency', '/fuel_efficency')
    ui.link('Back to home', '/')
@ui.page('/fuel_efficency_calculation')
def fuel_efficency_calculation_page():
    ui.colors(primary='#8B5CF6', accent='#C084FC')
    distance = ui.number("Distance (in meters)", value=1, min=1, step=1)
    fuel = ui.number("Fuel (in liters)", value=1, min=1, step=1)
    ui.button("Calculate", on_click=lambda: calculate_and_display_fuel_efficency(distance.value, fuel.value))
def calculate_and_display_fuel_efficency(distance, fuel):
    result = fuel_efficency_from_distance_and_fuel(distance, fuel)
    ui.label(f"The fuel efficency is {result['fuel_efficency']} meters per liter")
    ui.link('Back to Fuel Efficency', '/fuel_efficency')
    ui.link('Back to home', '/')
@ui.page('/distance_calculation')
def distance_calculation_page():
    ui.colors(primary='#8B5CF6', accent='#C084FC')
    fuel = ui.number("Fuel (in liters)", value=1, min=1, step=1)
    fuel_efficency = ui.number("Fuel efficency (in meters per liter)", value=1, min=1, step=1)
    ui.button("Calculate", on_click=lambda: calculate_and_display_distance(fuel.value, fuel_efficency.value))
def calculate_and_display_distance(fuel, fuel_efficency):
    result = distance_from_fuel_and_fuel_efficency(fuel, fuel_efficency)
    ui.label(f"The distance that can be traveled is {result['distance']} meters")
    ui.link('Back to Fuel Efficency', '/fuel_efficency')
    ui.link('Back to home', '/')
@ui.page('/rocket_stuff')
def rocket_stuff_page():
    ui.colors(primary='#8B5CF6', accent='#C084FC')
    ui.label("What do you wish to calculate among:")
    ui.button("Fall time", on_click=lambda: ui.navigate.to('/fall_time'))
    ui.button("Rocket maximum height", on_click=lambda: ui.navigate.to('/rocket_maximum_height'))
    ui.button("Ideal rocket equation", on_click=lambda: ui.navigate.to('/ideal_rocket_equation'))
    ui.button("Speed to escape gravity", on_click=lambda: ui.navigate.to('/escape_velocity'))
    ui.button("Delta mass", on_click=lambda: ui.navigate.to('/delta_mass'))
    ui.button("Terminal velocity", on_click=lambda: ui.navigate.to('/terminal_velocity'))
@ui.page('/fall_time')
def fall_time_page():
    ui.colors(primary='#8B5CF6', accent='#C084FC')
    ui.label("Do you want to inlude air resistance in the calculations?")
    ui.button("Yes", on_click=lambda: ui.navigate.to('/rocket_fall_time_adv'))
    ui.button("No", on_click=lambda: ui.navigate.to('/fall_time_basic'))
@ui.page('/fall_time_basic')
def fall_time_basic_page():
    ui.colors(primary='#8B5CF6', accent='#C084FC')
    height=ui.number("height?", value=1, min=1, step=1)
    fall_time_button=ui.button("Calculate", on_click=lambda: calculate_fall_time(height.value))
    ui.link('Back to rocket stuff', '/rocket_stuff')
    ui.link('Back to home', '/')
def calculate_fall_time(height):
    result = fall_simulation(height)
    speed = 9.81 * result
    ui.label(f"The maximum fall speed/impact speed of the rocket is {speed} and the time taken to fall is {result}")
@ui.page('/rocket_fall_time_adv')
def rocket_fall_time_page():
    ui.colors(primary='#8B5CF6', accent='#C084FC')
    height=ui.number("height of the rocket?", value=1, min=1, step=1)
    cross_sectional_area=ui.number("cross sectional area=", value=1, min=0.1, step=0.1)
    drag_coefficient=ui.number("drag coefficient=", value=0.47, min=0.01, step=0.01)
    ui.label("e.g. 0.47 for a smooth sphere, 1.05 for a cube, 1.28 for a flat plate and 0.04 for a streamlined body")
    ui.label("note, the drag coefficient is a dimensionless number that describes the drag force on an object moving through a fluid")
    phi=ui.number("density of the air (kg/m^3)", value=1.225, min=0.01, step=0.01)
    ui.label("At sea level")
    mass=ui.number("mass of the rocket? (kg)", value=100, min=0.1, step=10)
    gravity=ui.number("gravity? (N/kg)", value=9.81, min=0.1, step=0.1)
    time_step=ui.number("time step? (seconds)", value=0.1, step=0.01)
    ui.label("note, the smaller the time step, the more accurate the simulation. The longer the time step the sooner the simulation will be done note: please make sure the 1/time step is not reccuring")
    scale_height=ui.number("scale height of the atmosphere (m)", value=8500, min=0.1, step=100)
    ui.label("note, the scale height is the height at which the density of the atmosphere decreases by a factor of e (approximately 2.71828). The scale height is used to model the decrease in air density with altitude.")
    ui.button("Calculate", on_click=lambda: calculate_2(height.value, cross_sectional_area.value, drag_coefficient.value, phi.value, mass.value, gravity.value, time_step.value, scale_height.value))
def calculate_2(height, cross_sectional_area, drag_coefficient, phi, mass, gravity, time_step, scale_height):
    if time_step <= 0:
        ui.notify("Time step cannot be less than or equal to zero")
        ui.link('Back to home', '/')
    else:
        fall_simulation_advanced(height, cross_sectional_area, drag_coefficient, phi, mass, gravity, time_step, scale_height)
@ui.page('/rocket_maximum_height')
def rocket_maximum_height_page():
    ui.colors(primary='#8B5CF6', accent='#C084FC')
    gravity=ui.number("gravity (N/Kg)", value=9.81, min=0.1, step=0.1)
    time_step=ui.number("time step? (seconds)", value=0.1, step=0.01)
    ui.label("note, the smaller the time step, the more accurate the simulation. The longer the time step the sooner the simulation will be done note: please make sure the 1/time step is not reccuring and also remember that an extremly small time step will take ages to calculate")
    fuel=ui.number("fuel of the rocket? (kg)", value=1000, min=0.1, step=100)
    burn_rate=ui.number("burn rate? (kg/s)", value=10, min=0.1, step=1)
    thrust=ui.number("thrust of the rocket? (N)", value=10792, min=0.1, step=100)
    ui.label("note, the thrust must be greater than the weight of the rocket (g*(fuel+dry_mass))")
    dry_mass=ui.number("dry mass of the rocket? (kgs)", value=100, min=0.1, step=10)
    phi=ui.number("density of the air (kg/m^3)", value=1.225, min=0.01, step=0.01)
    ui.label("At sea level")
    drag_coefficient=ui.number("drag coefficient=", value=0.47, min=0.01, step=0.01)
    ui.label("e.g. 0.47 for a smooth sphere, 1.05 for a cube, 1.28 for a flat plate and 0.04 for a streamlined body")
    cross_sectional_area=ui.number("cross sectional area=", value=1, min=0.1, step=0.1)
    scale_height=ui.number("scale height of the atmosphere (m)", value=8500, min=0.1, step=100)
    ui.label("note, the scale height is the height at which the density of the atmosphere decreases by a factor of e (approximately 2.71828). The scale height is used to model the decrease in air density with altitude.")
    ui.button("Calculate maximum height", on_click=lambda: calculate(scale_height.value, phi.value, drag_coefficient.value, cross_sectional_area.value, fuel.value, burn_rate.value, thrust.value, gravity.value, time_step.value, dry_mass.value))
def calculate(scale_height, phi, drag_coefficient, cross_sectional_area, fuel, burn_rate, thrust, gravity, time_step, dry_mass):
    if time_step <= 0:
        ui.notify("Time step cannot be less than or equal to zero")
        ui.link('Back to rocket stuff', '/rocket_stuff')
        ui.link('Back to home', '/')
    else:
        wet_mass=fuel+dry_mass
        if thrust <= gravity * wet_mass:
            ui.notify("Thrust must be greater than the weight of the rocket (g*(fuel+dry_mass))")
            ui.link('Back to rocket stuff', '/rocket_stuff')
            ui.link('Back to home', '/')
        else:
            rocket_maximum_height_advanced(scale_height, phi, drag_coefficient, cross_sectional_area, fuel, burn_rate, thrust, gravity, time_step, dry_mass)
@ui.page('/ideal_rocket_equation')
def ideal_rocket_equation_page():
    ui.colors(primary='#8B5CF6', accent='#C084FC')
    isp=ui.number("Specific impulse (s)", value=300, min=0.1, step=1)
    initial_mass=ui.number("Initial mass (kg)", value=1000, min=0.1, step=10)
    final_mass=ui.number("Final mass (kg)", value=500, min=0.1, step=10)
    ui.button("Calculate delta-v", on_click=lambda: calculate_ideal_rocket_equation(isp.value, initial_mass.value, final_mass.value))
def calculate_ideal_rocket_equation(isp, initial_mass, final_mass):
    result = ideal_rocket_equation(isp, initial_mass, final_mass)
    ui.label(f"The delta-v of the rocket is {result['delta_v']} m/s")
    ui.link('back to rocket stuff', '/rocket_stuff')
    ui.link('Back to home', '/')
@ui.page('/escape_velocity')
def escape_velocity_page():
    ui.colors(primary='#8B5CF6', accent='#C084FC')
    gravity=ui.number("Gravity (N/kg)", value=9.81, min=0.1, step=0.1)
    radius=ui.number("Radius (m)", value=6371000, min=0.1, step=100)
    ui.button("Calculate escape velocity", on_click=lambda: calculate_escape_velocity(gravity.value, radius.value))
def calculate_escape_velocity(gravity, radius):
    result = escape_velocity(gravity, radius)
    ui.label(f"The escape velocity is {result['escape_velocity']} m/s")
    ui.link('back to rocket stuff', '/rocket_stuff')
    ui.link('Back to home', '/')
@ui.page('/delta_mass')
def delta_mass_page():
    ui.colors(primary='#8B5CF6', accent='#C084FC')
    initial_mass=ui.number("Initial mass (kg)", value=1000, min=0.1, step=10)
    final_mass=ui.number("Final mass (kg)", value=500, min=0.1, step=10)
    ui.button("Calculate delta mass", on_click=lambda: calculate_delta_mass(initial_mass.value, final_mass.value))
def calculate_delta_mass(initial_mass, final_mass):
    if final_mass > initial_mass:
        ui.notify("Final mass cannot be greater than initial mass")
        ui.link('back to rocket stuff', '/rocket_stuff')
        ui.link('Back to home', '/')
    else:
        result = delta_mass(initial_mass, final_mass)
        ui.label(f"The delta mass is {result['delta_mass']} kg")
        ui.link('back to rocket stuff', '/rocket_stuff')
        ui.link('Back to home', '/')
@ui.page('/terminal_velocity')
def terminal_velocity_page():
    ui.colors(primary='#8B5CF6', accent='#C084FC')
    mass=ui.number("Mass (kg)", value=100, min=0.1, step=10)
    gravity=ui.number("Gravity (N/kg)", value=9.81, min=0.1, step=0.1)
    drag_coefficient=ui.number("Drag coefficient", value=0.47, min=0.01, step=0.01)
    cross_sectional_area=ui.number("Cross sectional area (m^2)", value=1, min=0.1, step=0.1)
    phi=ui.number("Density of the air (kg/m^3)", value=1.225, min=0.01, step=0.01)
    ui.button("Calculate terminal velocity", on_click=lambda: calculate_terminal_velocity(mass.value, gravity.value, drag_coefficient.value, cross_sectional_area.value, phi.value))
def calculate_terminal_velocity(mass, gravity, drag_coefficient, cross_sectional_area, phi):
    result = terminal_velocity(mass, gravity, drag_coefficient, cross_sectional_area, phi)
    ui.label(f"The terminal velocity is {result['terminal_velocity']} m/s")
    ui.link('back to rocket stuff', '/rocket_stuff')
    ui.link('Back to home', '/')
@ui.page('/basic_calculus')
def basic_calculus_page():
    ui.colors(primary='#8B5CF6', accent='#C084FC')
    ui.label("what do you wish to calculate among:")
    ui.button("Derivative", on_click=lambda: ui.navigate.to('/derivatives'))
    ui.button("indefinite integral", on_click=lambda: ui.navigate.to('/indefinite_integrals'))
    ui.button("definite integral", on_click=lambda: ui.navigate.to('/definite_integrals'))
@ui.page('/derivatives')
def derivative_page():
    ui.colors(primary='#8B5CF6', accent='#C084FC')
    function=ui.input("What is the function?", value="x^2")
    ui.label("Note: use * instead of leaving the space between x and multiplier ")
    ui.button("Calcualte", on_click=lambda: calculate_derivative(function.value))
def calculate_derivative(function):
    x=sp.symbols('x')
    ans=sp.diff(function)
    readable=lambda ans: str(ans)
    ui.label(f"The derivative is {readable(ans)}")
    ui.link("Back to basic calculus", '/basic_calculus')
    ui.link("back to home", '/')
@ui.page('/indefinite_integrals')
def indefinite_integrals_page():
    ui.colors(primary='#8B5CF6', accent='#C084FC')
    function=ui.input("What is the function?", value="x^2")
    ui.label("Note: use * instead of leaving the space between x and multiplier")
    ui.button("Calculate", on_click=lambda: calculate_indefinite_integral(function.value))
def calculate_indefinite_integral(function):
    x=sp.symbols('x')
    ans=sp.integrate(function)
    readable=lambda ans: str(ans)
    ui.label(f"The indefinite integral is {readable(ans)}")
    ui.link("Back to basic calculus", '/basic_calculus')
    ui.link("back to home", '/')
@ui.page('/definite_integrals')
def definite_integrals_page():
    ui.colors(primary='#8B5CF6', accent='#C084FC')
    function=ui.input("What is the function", value="x^2")
    ui.label("Note: use * instead of leaving the space between x and multiplier ")
    upper_limit=ui.number("What is the upper limit?", value=10)
    lower_limit=ui.number("What is the lower limit", value=5)
    ui.button("Calculate", on_click=lambda: calculate_definite_integral(function.value, upper_limit.value, lower_limit.value))
def calculate_definite_integral(function, upper_limit, lower_limit):
    function_sp=sp.sympify(function)
    x=sp.symbols('x')
    integrated=sp.integrate(function_sp, x)
    num1_ans=integrated.subs(x, upper_limit)
    num2_ans=integrated.subs(x, lower_limit)
    ans=num1_ans-num2_ans
    readable=lambda ans: str(ans)
    ui.label(f"The definite integral is {readable(ans)}")
    ui.link("Back to basic calculus", '/basic_calculus')
    ui.link("back to home", '/')
@ui.page('/info')
def info_page(): 
    ui.label("This calculator is made for doing calculations based on astroscience and especially rockets.")
    ui.label("It was created by Keith Pukhrambam from October 2026 till November 2026 and can still receive updates.")
    ui.label("Also, AI was only used to help Keith learn so mistakes are more likely than an AI model (though it analyzed the code).")
    ui.label("This calculator is made for educational purposes and is not intended for professional use.")
    ui.label("Note: All the variable boxes about the celestial bodies are initially based on earth.")
    ui.label("Updates:")
    ui.label("Version 1.0.0 (November 2026): Initial release with 16 calculations and a basic UI.")
    ui.link('Back to home', '/')
@app.get('/health')
def health_check():
    return PlainTextResponse('ok') 
ui.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)),
       title='Astrokalc',
       dark=True,
       favicon='🌌'
       )
