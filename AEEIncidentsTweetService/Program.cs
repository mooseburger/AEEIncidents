using System;
using System.Collections.Generic;
using System.Linq;
using System.ServiceProcess;
using System.Text;
using System.Threading.Tasks;
using HybridWindowsService;

namespace AEEIncidentsTweetService
{
    static class Program
    {
        /// <summary>
        /// The main entry point for the application.
        /// </summary>
        static void Main()
        {
            HybridServiceBase[] ServicesToRun;
            ServicesToRun = new HybridServiceBase[] 
            { 
                new Service1() 
            };
            HybridServiceBase.Run(ServicesToRun);
        }
    }
}
