import React, { useState } from 'react';
import { MenuIcon, UserIcon } from '@heroicons/react/outline'
import { Link } from 'react-router-dom';
import { Menu, Transition } from '@headlessui/react'
import Logo from '../img/SIRPA.svg'

function Nav() {

    return (
        <>
            <header className=' border-b-2 border-gray-200'>
                <div className='mx-auto flex max-w-7xl items-center justify-between p-4'>
                    <div className='flex items-center space-x-2'>
                        <Menu as='div' className='relative'>
                            {({ open }) => (
                                <>
                                    <Menu.Button>
                                        <MenuIcon className='flex appearance-none p-1 md:hidden w-10 h-10' />
                                    </Menu.Button>
                                    <Transition 
                                        show={open}
                                        enter='transform transition duration-100 ease-in'
                                        enterFrom='opacity-0 scale-05'
                                        enterTo='opacity-100 scale-100'
                                        leave='transform transition duration-75 ease-out'
                                        leaveFrom='opacity-100 scale-100'
                                        leaveTo='opacity-0 scale-95'
                                    >
                                        <Menu.Items className="origin-top-left absolute left-0 mt-2 w-56 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 divide-y divide-gray-100 focus:outline-none" static>
                                            <Menu.Item>
                                                {({ active }) => (
                                                    <Link to='/student' className={`flex items-center px-4 py-2 text-lg ${active && "bg-red-700 text-white"}`}>
                                                        <UserIcon className='mr-3 h-5 w-5' aria-hidden='true'/>
                                                        Perfil
                                                    </Link>
                                                )}
                                            </Menu.Item>
                                        </Menu.Items>
                                    </Transition>
                                </>
                            )}
                        </Menu>
                        <Link to="/">
                            <img src={Logo} alt='SIRPA Logo' className=' min-w-fit min-h-fit' />
                        </Link>
                        <p className='text-xl invisible xl:visible max-w-xs font-sans font-medium'>Sistema Integrado de Resgisto de Presenças em Aula</p>
                    </div>
                    <nav className='hidden items-end space-x-2 text-sm font-medium text-gray-800 md:flex'>
                        <Link className='px-4 py-2 rounded transition hover:bg-gray-100'>
                        Perfil
                        </Link>
                    </nav>
                    <nav className='flex items-center space-x-1 text-sm font-medium text-gray-800'>
                        <Link to="/logout" className='bg-red-600 rounded px-4 py-2 text-white transition hover:bg-red-700'>Logout</Link>
                    </nav>
                </div>
            </header>
        </>
    );
}

export default Nav;
