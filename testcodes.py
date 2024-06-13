def show_cost():
    #data = request.json
    ruid = 'vm-1'
    #result = str1 + " " + str2
    #qry = select cost from resource_cost where res_unique_id = 'vm-1';
    qry = "select cost from resource_cost where res_unique_id = ' " + ruid + "';"
    print(qry)

    #name = "santhosh"
    

    #print_stmt1 = "hello  " + name + " how are you"
    #print_stmt = "my name is " + name

    
show_cost()